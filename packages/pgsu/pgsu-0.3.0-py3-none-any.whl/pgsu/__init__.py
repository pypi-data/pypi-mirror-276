# -*- coding: utf-8 -*-
"""Connect to an existing PostgreSQL cluster as the `postgres` superuser and execute SQL commands."""
__version__ = '0.3.0'

import logging
import traceback
import os
from enum import IntEnum
import subprocess
import warnings

# By default, try "sudo" only when 'postgres' user exists
DEFAULT_POSTGRES_UNIX_USER = 'postgres'
try:
    import pwd
    pwd.getpwnam(DEFAULT_POSTGRES_UNIX_USER)
    DEFAULT_TRY_SUDO = True
except (KeyError, ModuleNotFoundError):
    # user not found or pwd module not found (=not Unix)
    DEFAULT_TRY_SUDO = False

DEFAULT_POSTGRES_SUPERUSER = 'postgres'
if os.name == 'nt':  # on windows
    DEFAULT_POSTGRES_SUPERUSER = os.getlogin()

DEFAULT_DSN = {
    'host':
    None,  # 'localhost' causes psql to connect via method 'host' instead of 'local'
    'port': 5432,
    'user': DEFAULT_POSTGRES_SUPERUSER,
    'password': None,
    'dbname': 'template1',
}

LOGGER = logging.getLogger('pgsu')
LOGGER.setLevel(logging.DEBUG)


class PostgresConnectionMode(IntEnum):
    """Describe mode of connecting to postgres."""

    DISCONNECTED = 0
    PSYCOPG = 1
    PSQL = 2


class PGSU:
    """
    Connect to an existing PostgreSQL cluster as the `postgres` superuser and execute SQL commands.

    Tries to use psycopg with a fallback to psql subcommands (using ``sudo su`` to run as postgres user).

    Simple Example::

        pgsu = PGSU()
        pgsu.execute("CREATE USER testuser PASSWORD 'testpw'")

    Complex Example::

        pgsu = PGSU(interactive=True, dsn={'port': 5433})
        pgsu.execute("CREATE USER testuser PASSWORD 'testpw'")

    Note: In PostgreSQL
     * you cannot drop databases you are currently connected to
     * 'template0' is the unmodifiable template database (which you *cannot* connect to)
     * 'template1' is the modifiable template database (which you *can* connect to)
    """
    def __init__(self,
                 interactive=False,
                 quiet=True,
                 dsn=None,
                 determine_setup=True,
                 try_sudo=DEFAULT_TRY_SUDO,
                 postgres_unix_user=DEFAULT_POSTGRES_UNIX_USER):
        """Store postgres connection info.

        :param interactive: use True for verdi commands
        :param quiet: use False to show warnings/exceptions
        :param dsn: psycopg dictionary containing keys like 'host', 'user', 'port', 'dbname'.
            It is sufficient to provide only those values that deviate from the defaults.
        :param determine_setup: Whether to determine setup upon instantiation.
            You may set this to False and use the 'determine_setup()' method instead.
        :param try_sudo: If connection via psycopg fails, whether to try and use `sudo` to  become
            the `postgres_unix_user` and run commands using passwordless `psql`.
        :param postgres_unix_user: UNIX user to try to "become", if connection via psycopg fails
        """
        self.interactive = interactive
        if not quiet:
            handler = logging.StreamHandler()
            handler.setLevel(logging.INFO)
            LOGGER.addHandler(handler)
        self.connection_mode = PostgresConnectionMode.DISCONNECTED

        self.setup_fail_counter = 0
        self.setup_max_tries = 1

        self.dsn = DEFAULT_DSN.copy()
        if dsn is not None:
            self.dsn.update(dsn)

        if 'database' in self.dsn:
            warnings.warn(
                'The dsn contained the key `database` which was renamed to `dbname` in psycopg v3. '
                'Renamed the database key to dbname', UserWarning)
            self.dsn['dbname'] = self.dsn.pop('database')

        self.try_sudo = try_sudo
        self.postgres_unix_user = postgres_unix_user

        if determine_setup:
            self.determine_setup()

    def execute(self, command, **kwargs):
        """Execute postgres command using determined connection mode.

        :param command: A psql command line as a str
        :param kwargs: will be forwarded to _execute_... function
        """
        # Use self.dsn as default kwargs, update with provided dsn
        dsn = self.dsn.copy()
        dsn.update(kwargs)

        if self.connection_mode == PostgresConnectionMode.PSYCOPG:
            return _execute_psyco(command, dsn)
        if self.connection_mode == PostgresConnectionMode.PSQL:
            return _execute_su_psql(command, dsn)

        raise ConnectionError(
            'Could not connect to PostgreSQL server using dsn={dsn}.\n' \
                + 'Consider providing connection parameters via PGSU(dsn={...}).')

    def determine_setup(self):
        """Determine how to connect as the postgres superuser.

        Depending on how postgres is set up, psycopg can be used to create dbs and db users,
        otherwise a subprocess has to be used that executes psql as an os user with appropriate permissions.

        Note: We aim to connect as a superuser (typically 'postgres') with privileges to manipulate (create/drop)
          databases and database users.

        :returns success: True, if connection could be established.
        :rtype success: bool
        """
        dsn = self.dsn.copy()

        # Try to connect as a postgres superuser via psycopg (equivalent to using psql).
        LOGGER.debug('Trying to connect via "psycopg"...')
        for pg_user in unique_list([self.dsn.get('user'), None]):
            dsn['user'] = pg_user
            # First try the host specified (works if 'host' has setting 'trust' in pg_hba.conf).
            # Then try local connection (works if 'local' has setting 'trust' in pg_hba.conf).
            # Then try 'host' localhost via TCP/IP.
            for pg_host in unique_list([self.dsn.get('host'), None, 'localhost']):   # yapf: disable
                dsn['host'] = pg_host

                if _try_connect_psycopg(**dsn):
                    self.dsn = dsn
                    self.connection_mode = PostgresConnectionMode.PSYCOPG
                    return True

        # Ubuntu uses setting 'peer' for 'local', i.e. we need to be UNIX user 'postgres' in order to connect as
        # database user 'postgres'.
        # Check if 'sudo' is available and try to become 'postgres'.
        if self.try_sudo:
            LOGGER.debug('Trying to connect by becoming the "%s" unix user...',
                         self.postgres_unix_user)
            if _sudo_exists():
                dsn = self.dsn.copy()
                dsn['user'] = self.postgres_unix_user

                if _try_su_psql(interactive=self.interactive, dsn=dsn):
                    self.dsn = dsn
                    self.connection_mode = PostgresConnectionMode.PSQL
                    return True
            else:
                LOGGER.info(
                    'Could not find `sudo` to become the the "%s" unix user.',
                    self.postgres_unix_user)

        self.setup_fail_counter += 1
        return self._no_setup_detected()

    def _no_setup_detected(self):
        """Print a warning message and calls the failed setup callback

        :returns: False, if no successful try.
        """
        LOGGER.warning('Unable to autodetect postgres setup.')

        if self.interactive and self.setup_fail_counter <= self.setup_max_tries:
            self.dsn = prompt_for_dsn(self.dsn)
            return self.determine_setup()

        return False

    @property
    def is_connected(self):
        """Whether successful way of connecting to PostgreSQL cluster has been determined.
        """
        return self.connection_mode in (PostgresConnectionMode.PSYCOPG,
                                        PostgresConnectionMode.PSQL)


def prompt_for_dsn(dsn):
    """
    Prompt interactively for postgres database connection details.

    :return: dictionary with the keys: host, port, database, user, password
    """
    import click  # pylint: disable=import-outside-toplevel
    click.echo('Please provide PostgreSQL connection info:')

    # Note: Using '' as the prompt default is necessary to allow users to leave the field empty.
    #       Using `None` in the dictionary is necessary in order for  to interpret the value as not provided.
    dsn_new = {}
    dsn_new['host'] = click.prompt(
        'postgres host', default=dsn.get('host') or '', type=str) or None
    dsn_new['port'] = click.prompt(
        'postgres port', default=dsn.get('port'), type=int) or None
    dsn_new['user'] = click.prompt(
        'postgres super user', default=dsn.get('user'), type=str) or None
    dsn_new['dbname'] = click.prompt(
        'dbname', default=dsn.get('dbname'), type=str) or None
    dsn_new['password'] = click.prompt(
        'postgres password of {dsn_new["user"]}',
        #hide_input=True,   # this breaks the input mocking in the tests. could make this configurable instead
        type=str,
        default=dsn.get('password') or '') or None

    return dsn_new


def _try_connect_psycopg(**kwargs):
    """
    try to start a psycopg connection.

    :return: True if successful, False otherwise
    """
    from psycopg import connect  # pylint: disable=import-outside-toplevel
    success = False
    try:
        conn = connect(**kwargs)
        success = True
        conn.close()
    except Exception:  # pylint: disable=broad-except
        LOGGER.debug('Unable to connect via psycopg')
        LOGGER.debug(traceback.format_exc())
    return success


def _execute_psyco(command, dsn):
    """
    executes a postgres commandline through psycopg

    :param command: A psql command line as a str
    :param dsn: will be forwarded to psycopg.connect
    """
    import psycopg  # pylint: disable=import-outside-toplevel

    conn = None
    output = None
    try:
        conn = psycopg.connect(**dsn)
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(command)
            if cursor.description is not None:
                output = cursor.fetchall()
    finally:
        if conn:
            conn.close()
    return output


def _sudo_exists():
    """
    Check that the sudo command can be found

    :return: True if successful, False otherwise
    """
    try:
        subprocess.check_output(['sudo', '-V'])
        return True
    except (subprocess.CalledProcessError, OSError):
        LOGGER.debug('Failed to run "sudo" in a subprocess')
        LOGGER.debug(traceback.format_exc())

    return False


def _try_su_psql(interactive, dsn):
    """
    Try to run psql in a subprocess as a different UNIX user.

    :return: True if successful, False otherwise
    """
    try:
        _execute_su_psql(r'\q', interactive=interactive, dsn=dsn)
        return True
    except subprocess.CalledProcessError:
        LOGGER.debug('Failed to run "psql" in a subprocess as user %s',
                     dsn.get('user'))
        LOGGER.debug(traceback.format_exc())
    return False


def _execute_su_psql(command, dsn, interactive=False):
    """
    Executes an SQL command via ``psql`` as another system user in a subprocess.

    Tries to "become" the user specified in ``dsn`` (i.e. interpreted as UNIX system user)
    and run psql in a subprocess.

    Logs any output on 'stderr' to the pgsu logger at 'warning' level.

    :param command: A psql command line as a str
    :param dsn: connection details to forward to psql, signature as in psycopg.connect
    :param interactive: If False, `sudo` won't ask for a password and fail if one is required.
    """
    psql_option_str = ''

    if 'database' in dsn:
        warnings.warn(
            'The dsn contained the key `database` which was renamed to `dbname` in psycopg v3. '
            'Renamed the database key to dbname', UserWarning)
        dsn['dbname'] = dsn.pop('database')

    dbname = dsn.get('dbname')
    if dbname:
        psql_option_str += f'-d {dbname}'

    # to do: Forward password to psql; ignore host only when the password is None.  # pylint: disable=fixme
    # Note: There is currently no known postgresql setup that needs this, though
    # password = dsn.get('password')

    host = dsn.pop('host', 'localhost')
    if host and host != 'localhost':
        psql_option_str += f' -h {host}'
    else:
        LOGGER.debug(
            "Found host 'localhost' but dropping '-h localhost' option for psql "
            'since this may cause psql to switch to password-based authentication.'
        )

    port = dsn.get('port')
    if port:
        psql_option_str += f' -p {port}'

    # Note: This is *both* the UNIX user to become *and* the database user
    user = dsn.get('user')

    # Build command line
    sudo_cmd = ['sudo']
    if not interactive:
        sudo_cmd += ['-n']
    su_cmd = ['su', user, '-c']

    # Note: cd to home directory of user. Otherwise psql can fail with
    # "could not change directory to ...: Permission denied"
    psql_cmd = [
        f'cd ~ && psql {psql_option_str} -tc {escape_for_bash(command)}'
    ]
    sudo_su_psql = sudo_cmd + su_cmd + psql_cmd

    LOGGER.info(
        "Trying to become '%s' user. You may be asked for your 'sudo' password.",
        user)

    # This block implements 'result = check_output(sudo_su_psql, encoding="utf-8")',
    # except that we capture stderr and log it.
    proc = subprocess.run(
        sudo_su_psql,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='utf-8',
        check=False,
    )
    if proc.stderr:
        LOGGER.warning(proc.stderr)
    proc.check_returncode()
    result = proc.stdout

    result = result.strip().split(os.linesep)
    result = [i for i in result if i]

    return result


def escape_for_bash(str_to_escape):
    """
    This function takes any string and escapes it in a way that
    bash will interpret it as a single string.

    Explanation:

    At the end, in the return statement, the string is put within single
    quotes. Therefore, the only thing that I have to escape in bash is the
    single quote character. To do this, I substitute every single
    quote ' with '"'"' which means:

    First single quote: exit from the enclosing single quotes

    Second, third and fourth character: "'" is a single quote character,
    escaped by double quotes

    Last single quote: reopen the single quote to continue the string

    Finally, note that for python I have to enclose the string '"'"'
    within triple quotes to make it work, getting finally: the complicated
    string found below.
    """
    escaped_quotes = str_to_escape.replace("'", """'"'"'""")
    return f"'{escaped_quotes}'"


def unique_list(non_unique_list):
    """
    Return list with unique subset of provided list, maintaining list order.
    Source: https://stackoverflow.com/a/480227/1069467
    """
    seen = set()
    return [x for x in non_unique_list if not (x in seen or seen.add(x))]
