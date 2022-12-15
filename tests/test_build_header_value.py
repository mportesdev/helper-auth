import pytest

from helper_auth import HelperAuth


def test_default():
    auth = HelperAuth("helper")
    result = auth._build_header_value("username=github_name\npassword=github_token\n")
    assert result == "token github_token"


def test_custom_key():
    auth = HelperAuth("helper", key="auth")
    result = auth._build_header_value("username=github_name\nauth=github_token\n")
    assert result == "token github_token"


def test_custom_prefix():
    auth = HelperAuth("helper", prefix="Bearer ")
    result = auth._build_header_value("username=github_name\npassword=github_token\n")
    assert result == "Bearer github_token"


def test_missing_key_raises_error():
    auth = HelperAuth("helper")
    with pytest.raises(KeyError, match="helper did not provide the key 'password'"):
        auth._build_header_value("username=github_name\nauth=github_token\n")
