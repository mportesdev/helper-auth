from unittest.mock import patch

import pytest

from helper_auth import HelperAuth


def test_default():
    auth = HelperAuth("helper")
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "username=github_name\npassword=github_token\n"
        assert auth._get_token() == "github_token"


def test_space_delimited_helper_output():
    auth = HelperAuth("helper")
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = (
            "username = github_name\npassword = github_token\n"
        )
        assert auth._get_token() == "github_token"


def test_custom_key():
    auth = HelperAuth("helper", key="token")
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "username=github_name\ntoken=github_token\n"
        assert auth._get_token() == "github_token"


def test_missing_key_raises_error():
    auth = HelperAuth("helper")
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "username=github_name\nauth=github_token\n"
        with pytest.raises(KeyError, match="helper did not provide the key 'password'"):
            auth._get_token()
