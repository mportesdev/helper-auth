import contextlib
import subprocess

try:
    from requests.auth import AuthBase
except ModuleNotFoundError:

    class AuthBase:
        """Base class for authentication handlers."""


class HelperAuth(AuthBase):
    def __init__(
        self,
        command,
        key="password",
        prefix="token ",
        header="Authorization",
        cache_token=False,
    ):
        self._command = _ensure_list(command)
        self._key = key
        self._prefix = prefix
        self._header = header
        self._cache_token = cache_token
        self._token = None

    def __call__(self, request):
        request.headers[self._header] = f"{self._prefix}{self._get_token()}"
        return request

    def _get_token(self):
        if self._token is not None:
            return self._token
        helper_output = subprocess.run(
            self._command, capture_output=True, check=True, encoding="utf-8", text=True
        ).stdout
        token = self._token_from_helper_output(helper_output)
        if self._cache_token:
            self._token = token
        return token

    def _token_from_helper_output(self, helper_output):
        for line in helper_output.strip().splitlines():
            try:
                key, value = line.split("=", maxsplit=1)
            except ValueError:
                continue
            if key.strip() == self._key:
                return value.strip()
        raise KeyError(f"helper did not provide the key {self._key!r}")

    def clear_cache(self):
        """Clear the cached token."""
        self._token = None


def _ensure_list(command):
    with contextlib.suppress(AttributeError):
        # path-like: convert to string
        command = command.__fspath__()
    with contextlib.suppress(AttributeError):
        # string: split to list
        command = command.split()
    return command
