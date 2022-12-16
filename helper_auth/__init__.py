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
        return f"{self.prefix}{self._token_from_helper_output(command_stdout)}"

    def _token_from_helper_output(self, helper_output):
        for line in helper_output.strip().splitlines():
            key, value = line.split("=", maxsplit=1)
            if key.strip() == self.key:
                return value.strip()
        raise KeyError(f"helper did not provide the key {self.key!r}")


def _ensure_list(command):
    with contextlib.suppress(AttributeError):
        # path-like: convert to string
        command = command.__fspath__()
    with contextlib.suppress(AttributeError):
        # string: split to list
        command = command.split()
    return command
