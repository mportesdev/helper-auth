[![helper-auth on PyPI][PyPI badge]][PyPI page]

This Python library provides the `HelperAuth` class whose objects are intended
to be used as custom authentication handlers in conjunction with
the [Requests] library, as suggested in its [documentation].


# Installation

```
pip install helper-auth
```

Please note that while `helper-auth` is supposed to be used in
environments with `requests` installed, it does not depend on it.
To install `requests` together with `helper-auth`, specify it as an extra:

```
pip install 'helper-auth[requests]'
```


# Usage

Suppose you have an existing GitHub personal access token, and
a [Git credential helper] already set up for Git to authenticate to
GitHub using this token as the password. This helper prints the following
to standard output:

```
$ git credential-github
username=your_github_username
password=your_github_token
```

You want to use the same token to make GitHub API calls using the Requests
library. The API expects a `token your_github_token` string as the value of
your request's `Authorization` header.

You can use `HelperAuth` with its default settings:

```python
import requests
from helper_auth import HelperAuth

auth = HelperAuth("git credential-github")

response = requests.get("https://api.github.com/user", auth=auth)
```


## Specifying the helper command

The helper command can be specified as one or more positional arguments.
The following are all valid:

```python
auth = HelperAuth("helper")
```

```python
auth = HelperAuth("helper --option arg")
```

```python
auth = HelperAuth("helper", "--option", "arg")
```

In addition, the first positional argument can be a path-like object:

```python
auth = HelperAuth(Path("helper"))
```

```python
auth = HelperAuth(Path("helper"), "--option", "arg")
```


## Caching the token

By default, a `HelperAuth` object never stores the value of the token
(password) in its internal state. Rather, the helper command is invoked
each time the object is called. This is an intentional precaution (such
that the token cannot be retrieved *ex post* by the introspection of the
`HelperAuth` object) but it can also be unnecessarily expensive if the object
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
[Requests]: https://requests.readthedocs.io
[documentation]: https://requests.readthedocs.io/en/latest/user/authentication/#new-forms-of-authentication
[Git credential helper]: https://git-scm.com/docs/gitcredentials#_custom_helpers
