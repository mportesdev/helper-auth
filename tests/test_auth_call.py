from unittest.mock import patch

import pytest
from pytest_cases import parametrize_with_cases

from helper_auth import HelperAuth
from . import HelperOutputCases


class Request:
    def __init__(self):
        self.headers = {}


@parametrize_with_cases("helper_output", cases=HelperOutputCases)
def test_default_key(helper_output):
    auth = HelperAuth("helper")
    request = Request()

    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = helper_output
        auth(request)

    assert request.headers["Authorization"] == "token GITHUB_TOKEN"


def test_custom_key():
    auth = HelperAuth("helper", key="token")
    request = Request()

    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "username=GITHUB_NAME\ntoken=GITHUB_TOKEN\n"
        auth(request)

    assert request.headers["Authorization"] == "token GITHUB_TOKEN"


def test_custom_prefix():
    auth = HelperAuth("helper", prefix="Bearer ")
    request = Request()

    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "username=GITHUB_NAME\npassword=GITHUB_TOKEN\n"
        auth(request)

    assert request.headers["Authorization"] == "Bearer GITHUB_TOKEN"


def test_custom_header():
    auth = HelperAuth("helper", header="X-Auth")
    request = Request()

    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "username=GITHUB_NAME\npassword=GITHUB_TOKEN\n"
        auth(request)

    assert request.headers["X-Auth"] == "token GITHUB_TOKEN"


def test_missing_key_raises_error():
    auth = HelperAuth("helper")
    request = Request()

    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "username=GITHUB_NAME\nauth=GITHUB_TOKEN\n"
        with pytest.raises(KeyError, match="helper did not provide the key 'password'"):
            auth(request)


def test_token_not_cached_by_default():
    auth = HelperAuth("helper")

    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "username=GITHUB_NAME\npassword=GITHUB_TOKEN\n"
        auth(Request())

    assert auth._token is None


def test_token_cached_optionally():
    auth = HelperAuth("helper", cache_token=True)

    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "username=GITHUB_NAME\npassword=GITHUB_TOKEN\n"
        auth(Request())

    assert auth._token == "GITHUB_TOKEN"
