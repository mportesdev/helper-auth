import pytest

from helper_auth import HelperAuth


def test_default():
    auth = HelperAuth("helper")
    assert (
        auth._token_from_helper_output("username=github_name\npassword=github_token\n")
        == "github_token"
    )


def test_space_delimited_helper_output():
    auth = HelperAuth("helper")
    assert (
        auth._token_from_helper_output(
            "username = github_name\npassword = github_token\n"
        )
        == "github_token"
    )


def test_custom_key():
    auth = HelperAuth("helper", key="auth")
    assert (
        auth._token_from_helper_output("username=github_name\nauth=github_token\n")
        == "github_token"
    )


def test_missing_key_raises_error():
    auth = HelperAuth("helper")
    with pytest.raises(KeyError, match="helper did not provide the key 'password'"):
        auth._token_from_helper_output("username=github_name\nauth=github_token\n")


def test_empty_line_ignored():
    auth = HelperAuth("helper")
    assert (
        auth._token_from_helper_output(
            "username=github_name\n\npassword=github_token\n"
        )
        == "github_token"
    )


def test_unexpected_line_ignored():
    auth = HelperAuth("helper")
    assert (
        auth._token_from_helper_output(
            "# comment\nusername=github_name\npassword=github_token\n"
        )
        == "github_token"
    )
