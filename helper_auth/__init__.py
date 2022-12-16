import contextlib
import subprocess

from requests.auth import AuthBase


class HelperAuth(AuthBase):
    def __init__(
        self,
        command,
        key="password",
        prefix="token ",
        header="Authorization",
        cache_token=False,
    ):
        self.command = _ensure_list(command)
        self.key = key
        self.prefix = prefix
        self.header = header
        self.cache_token = cache_token
        self._token = None

    def __call__(self, request):
        request.headers[self.header] = f"{self.prefix}{self._get_token()}"
        return request

    def _get_token(self):
        if self._token is not None:
            return self._token
        helper_output = subprocess.run(
            self.command, capture_output=True, check=True, encoding="utf-8", text=True
        ).stdout
        token = self._token_from_helper_output(helper_output)
        if self.cache_token:
            self._token = token
        return token

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
