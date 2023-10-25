from unittest.mock import patch

import pytest
from pytest_cases import parametrize_with_cases

from helper_auth import HelperAuth

from . import HelperOutputCases


@parametrize_with_cases("helper_output", cases=HelperOutputCases)
def test_default_key(helper_output):
    auth = HelperAuth("helper")
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = helper_output
        assert auth._get_token() == "GITHUB_TOKEN"


def test_custom_key():
    auth = HelperAuth("helper", key="token")
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "username=GITHUB_NAME\ntoken=GITHUB_TOKEN\n"
        assert auth._get_token() == "GITHUB_TOKEN"


def test_missing_key_raises_error():
    auth = HelperAuth("helper")
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "username=GITHUB_NAME\nauth=GITHUB_TOKEN\n"
        with pytest.raises(KeyError, match="helper did not provide the key 'password'"):
            auth._get_token()


def test_token_not_cached_by_default():
    auth = HelperAuth("helper")
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "username=GITHUB_NAME\npassword=GITHUB_TOKEN\n"
        auth._get_token()
    assert auth._token is None


def test_command_always_invoked_by_default():
    auth = HelperAuth("helper")
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "username=GITHUB_NAME\npassword=GITHUB_TOKEN\n"
        auth._get_token()
        mock_run.assert_called_once()
        auth._get_token()
        assert mock_run.call_count == 2


def test_token_cached_optionally():
    auth = HelperAuth("helper", cache_token=True)
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "username=GITHUB_NAME\npassword=GITHUB_TOKEN\n"
        auth._get_token()
    assert auth._token == "GITHUB_TOKEN"  # nosec: B105


def test_command_invoked_only_once_when_token_cached():
    auth = HelperAuth("helper", cache_token=True)
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "username=GITHUB_NAME\npassword=GITHUB_TOKEN\n"
        auth._get_token()
        mock_run.assert_called_once()
        auth._get_token()
        mock_run.assert_called_once()


def test_token_containing_equals_sign():
    auth = HelperAuth("helper")
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "username=GITHUB_NAME\npassword=RxVlf=E9aRU+\n"
        assert auth._get_token() == "RxVlf=E9aRU+"
