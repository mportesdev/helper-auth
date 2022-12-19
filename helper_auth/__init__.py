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
        request.headers[self.header] = f"{self.prefix}{self._get_token()}"
        return request

    def _get_token(self):
        helper_output = subprocess.run(
            self.command, capture_output=True, check=True, encoding="utf-8", text=True
        ).stdout
        return self._token_from_helper_output(helper_output)

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
