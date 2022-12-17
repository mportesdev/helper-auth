from unittest.mock import patch

import pytest

from helper_auth import HelperAuth


class Request:
    def __init__(self):
        self.headers = {}


def test_default():
    auth = HelperAuth("helper")
    request = Request()

    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "username=github_name\npassword=github_token\n"
        auth(request)

    assert request.headers["Authorization"] == "token github_token"


def test_space_delimited_helper_output():
    auth = HelperAuth("helper")
    request = Request()

    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = (
            "username = github_name\npassword = github_token\n"
        )
        auth(request)

    assert request.headers["Authorization"] == "token github_token"


def test_custom_key():
    auth = HelperAuth("helper", key="token")
    request = Request()

    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "username=github_name\ntoken=github_token\n"
        auth(request)

    assert request.headers["Authorization"] == "token github_token"


def test_custom_prefix():
    auth = HelperAuth("helper", prefix="Bearer ")
    request = Request()

    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "username=github_name\npassword=github_token\n"
        auth(request)

    assert request.headers["Authorization"] == "Bearer github_token"


def test_custom_header():
    auth = HelperAuth("helper", header="X-Auth")
    request = Request()

    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "username=github_name\npassword=github_token\n"
        auth(request)

    assert request.headers["X-Auth"] == "token github_token"


def test_missing_key_raises_error():
    auth = HelperAuth("helper")
    request = Request()

    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "username=github_name\nauth=github_token\n"
        with pytest.raises(KeyError, match="helper did not provide the key 'password'"):
            auth(request)


def test_token_not_stored_by_default():
    auth = HelperAuth("helper")

    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "username=github_name\npassword=github_token\n"
        auth(Request())

    assert auth._token is None


def test_command_always_invoked_by_default():
    auth = HelperAuth("helper")

    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "username=github_name\npassword=github_token\n"
        auth(Request())
        auth(Request())

    assert mock_run.call_count == 2


def test_token_stored_optionally():
    auth = HelperAuth("helper", cache_token=True)

    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "username=github_name\npassword=github_token\n"
        auth(Request())

    assert auth._token == "github_token"


def test_command_invoked_once_when_token_stored():
    auth = HelperAuth("helper", cache_token=True)

    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "username=github_name\npassword=github_token\n"
        auth(Request())
        auth(Request())

    assert mock_run.call_count == 1


def test_empty_line_ignored():
    auth = HelperAuth("helper")
    request = Request()

    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "username=github_name\n\npassword=github_token\n"
        auth(request)

    assert request.headers["Authorization"] == "token github_token"


def test_unexpected_line_ignored():
    auth = HelperAuth("helper")
    request = Request()

    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = (
            "# comment\nusername=github_name\npassword=github_token\n"
        )
        auth(request)

    assert request.headers["Authorization"] == "token github_token"
