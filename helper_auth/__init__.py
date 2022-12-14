import contextlib
import subprocess

from requests.auth import AuthBase


class HelperAuth(AuthBase):
    def __init__(
        self, command, key="password", prefix="token ", header="Authorization"
    ):
        self.command = _ensure_list(command)
        self.key = key
        self.prefix = prefix
        self.header = header

    def __call__(self, request):
        command_stdout = subprocess.run(
            self.command, capture_output=True, check=True, encoding="utf-8", text=True
        ).stdout

        request.headers[self.header] = self._build_header_value(command_stdout)
        return request

    def _build_header_value(self, command_stdout):
        for line in command_stdout.strip().splitlines():
            key, value = line.split("=", maxsplit=1)
            if key == self.key:
                return f"{self.prefix}{value}"


def _ensure_list(command):
    with contextlib.suppress(AttributeError):
        # path-like: convert to string
        command = command.__fspath__()
    with contextlib.suppress(AttributeError):
        # string: split to list
        command = command.split()
    return command
