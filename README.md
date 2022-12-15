[![helper-auth on PyPI](https://img.shields.io/pypi/v/helper-auth)][PyPI]

# Installation

```
pip install helper-auth
```

# Usage

Objects of the `HelperAuth` class are intended to be used as custom
authentication handlers as per the
[Requests documentation](https://requests.readthedocs.io/en/latest/user/authentication/#new-forms-of-authentication).


## Default scenario

Suppose you have an existing GitHub personal access token, and a
[Git credential helper](https://git-scm.com/docs/gitcredentials#_custom_helpers)
already set up for Git to authenticate to GitHub using this token as
the password. This helper is named `git-credential-github` and prints
the following to standard output:

```
username=your_github_username
password=your_github_token
```

You want to use the same token to make GitHub API calls in Python with
the help of the Requests library. The API expects a
`token your_github_token` string as the value of
your request's `Authorization` header.

You can use `HelperAuth` with its default settings:

```python
import requests
from helper_auth import HelperAuth

headers = {'Accept': 'application/vnd.github+json'}
auth = HelperAuth('git-credential-github')

response = requests.get(
    'https://api.github.com/user/repos',
    headers=headers,
    auth=auth,
)
```

[PyPI]: https://pypi.org/project/helper-auth
