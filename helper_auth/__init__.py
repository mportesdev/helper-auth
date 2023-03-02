import subprocess

try:
    from requests.auth import AuthBase
except ModuleNotFoundError:

    class AuthBase:
        """Base class for authentication handlers."""


__version__ = "0.7.0"


class HelperAuth(AuthBase):
    """Request authentication handler.

    `command` is the helper command to invoke. It may be a string or
    a path-like object. `args` are optional command-line arguments for
    this command.

    As a shortcut, a command with command-line arguments can also be
    passed as a single string, e.g. ``HelperAuth("helper --option arg")``
    is equivalent to ``HelperAuth("helper", "--option", "arg")``.

    `key` is the key string to search for in the "key=value" pairs
    in the helper output. Default is "password".

    `scheme` specifies the authentication scheme. Default is "Bearer".

    `header` is the request header that will be modified by the
    handler. Default is "Authorization".

    `cache_token` allows to cache the token value optionally to avoid
    repeated invocation of the helper command. Default is False.
    """

    def __init__(
        self,
        command,
        *args,
        key="password",
        scheme="Bearer",
        header="Authorization",
        cache_token=False,
    ):
        self._command = _ensure_list(command, *args)
        self._key = key
        self._scheme = scheme
        self._header = header
        self._cache_token = cache_token
        self._token = None

    def __call__(self, request):
        request.headers[self._header] = f"{self._scheme} {self._get_token()}"
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
            if key == self._key:
                return value
        raise KeyError(f"helper did not provide the key {self._key!r}")

    def clear_cache(self):
        """Clear the cached token."""
        self._token = None


def _ensure_list(command, *args):
    try:
        # if command is path-like, convert to filesystem representation
        return [command.__fspath__(), *args]
    except AttributeError:
        # otherwise split to handle single-string commands such as "helper --option"
        return [*command.split(), *args]
