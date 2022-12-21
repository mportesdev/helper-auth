import pytest
from pytest_cases import parametrize_with_cases

from helper_auth import HelperAuth
from . import HelperOutputCases


@parametrize_with_cases("helper_output", cases=HelperOutputCases)
def test_default_key(helper_output):
    auth = HelperAuth("helper")
    assert auth._token_from_helper_output(helper_output) == "github_token"


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
