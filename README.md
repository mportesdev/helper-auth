[![helper-auth on PyPI][PyPI badge]][PyPI page]


# Installation

```
pip install helper-auth
```


# Usage

Objects of the `HelperAuth` class are intended to be used as custom
authentication handlers as per the [Requests documentation].


## Default scenario

Suppose you have an existing GitHub personal access token, and a
[Git credential helper] already set up for Git
to authenticate to GitHub using this token as
the password. This helper prints the following to standard output:

```
$ git credential-github
username=your_github_username
password=your_github_token
```

You want to use the same token to make GitHub API calls in Python with
the help of the Requests library. The API expects a
`token your_github_token` string as the value of
your request's `Authorization` header.

You can use a `HelperAuth` authentication handler with its default settings:

```python
import requests
from helper_auth import HelperAuth

auth = HelperAuth("git credential-github")

response = requests.get("https://api.github.com/user/repos", auth=auth)
```


## Specifying the helper command

Simple helper command with no command-line arguments can be a string or
a path-like object.

```python
auth = HelperAuth("helper")
```

```python
auth = HelperAuth(Path("helper"))
```

If the helper command contains command-line arguments, it can be a string or
a list of strings.

```python
auth = HelperAuth("helper --option arg")
```

```python
auth = HelperAuth(["helper", "--option", "arg"])
```


## Caching the token

By default, a `HelperAuth` authentication handler never stores the value of
the token (password) in its internal state. Rather, the helper command is
invoked on each call to the handler. This is an intentional precaution
(such that the token cannot be retrieved *ex post* by the introspection
of the handler) but it can also be unnecessarily expensive if the handler
is to be called repeatedly, e.g. when making many simultaneous API calls.
You can override this behavior by passing `cache_token=True` to the
constructor:

```python
auth = HelperAuth("helper", cache_token=True)
```

The cached token can then be cleared anytime by calling

```python
auth.clear_cache()
```

[PyPI badge]: https://img.shields.io/pypi/v/helper-auth
[PyPI page]: https://pypi.org/project/helper-auth
[Requests documentation]: https://requests.readthedocs.io/en/latest/user/authentication/#new-forms-of-authentication
[Git credential helper]: https://git-scm.com/docs/gitcredentials#_custom_helpers
