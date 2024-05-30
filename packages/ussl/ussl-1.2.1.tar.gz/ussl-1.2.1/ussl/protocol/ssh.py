import io
import socket
import time
from typing import Optional, Self, Union

import paramiko
from paramiko.rsakey import RSAKey
from paramiko.ssh_exception import AuthenticationException, SSHException

from ..model import Protocol, Query, Response
from .base import BaseProtocol
from ..exceptions import ConnectionFailed, ExecutionError, CredentialsError


class SSHProtocol(BaseProtocol):
    name = 'ssh'
    """
    A class used to represent a ssh connection to remote host

    :param host: hostname or ip address of remote server
    :param login: user login for remote connection
    :param password: user password for remote connection
    :param port: ssh port. default 22 If not specified
    :param SSH_CONNECT_TIMEOUT: an optional timeout (in seconds)
        for the TCP connect
    :param EXEC_COMMAND_TIMEOUT: an optional timeout (in seconds)
        for execute command
    """

    SSH_CONNECT_TIMEOUT: int = 60
    EXEC_COMMAND_TIMEOUT: int = 60

    _connection: Optional[paramiko.SSHClient] = None

    def __init__(self, protocol: Optional[Protocol] = None):
        super().__init__(protocol)
        if not self._connection and protocol:
            self.connect()

    def connect(self):
        """Open SSH connection to remote host.

        :raises: CreateSSHConnectionError: if failed authentication
            or connection or establishing an SSH session
        """
        protocol = self.protocol
        host = protocol.host
        login = protocol.username
        domain = protocol.domain
        if domain is not None:
            login = f'{login}@{domain}'
        password = protocol.password
        port = protocol.port or 22
        ssh_key = protocol.pem_file
        try:
            self._connection = paramiko.SSHClient()
            self._connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if password:
                self._connection.connect(
                    hostname=host, username=login,
                    password=password, port=port,
                    look_for_keys=False, allow_agent=False,
                    timeout=SSHProtocol.SSH_CONNECT_TIMEOUT
                )
            elif ssh_key:
                keyfile = io.StringIO(ssh_key)
                self._connection.connect(
                    host, port, login,
                    pkey=RSAKey.from_private_key(keyfile),
                    timeout=SSHProtocol.SSH_CONNECT_TIMEOUT,
                    look_for_keys=False,
                    allow_agent=False
                )
        except AuthenticationException as error:
            raise CredentialsError(str(error))
        except (SSHException, socket.timeout) as exc:
            raise ConnectionFailed(str(exc))
        except Exception as error:
            raise ConnectionFailed(f'SSH connection failed: {error}')

    def close(self):
        """Close SSH connection."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def __enter__(self) -> Self:
        self.connect()
        return self

    def __exit__(self, exc_type: Exception, *args):
        self.close()  ## TODO: fix
        if exc_type is not None:
            return False
        return True

    def execute(self, query: Union[Query, str]) -> Response:
        if isinstance(query, str):
            query = Query(command=query)
        command = query.command
        sudo = query.sudo
        timeout = query.timeout if query.timeout else SSHProtocol.EXEC_COMMAND_TIMEOUT
        if self._connection is None:
            self.connect()
        stdin, stdout, err = self._connection.exec_command(
            command=command,
            timeout=timeout)
        if sudo:
            stdin.write(sudo + "\n")
            stdin.flush()
            time.sleep(1)
        stdout = stdout.read().decode('utf-8')
        error = err.read().decode('utf-8')
        if not stdout and error:
            if self.EXECUTE_ERROR_IGNORE:
                return Response(result=f'Command "{command}" executed failed',
                                status_code=1,
                                stderr=error,
                                stdout=stdout)
            raise ExecutionError(error + stdout + f'\nCommand: {command}')
        else:
            return Response(result='Command executed successfully',
                            status_code=0,
                            stdout=stdout,
                            stderr=error)
