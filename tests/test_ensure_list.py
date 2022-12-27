from pytest_cases import parametrize_with_cases
from pytest_cases.filters import id_has_suffix, id_match_regex

from helper_auth import _ensure_list


@parametrize_with_cases("command", filter=~id_match_regex(".*_with_arg"))
def test_ensure_list_without_args(command):
    assert _ensure_list(command) == ["helper"]


@parametrize_with_cases("command", filter=id_has_suffix("_with_arg"))
def test_ensure_list_with_one_arg(command):
    assert _ensure_list(command) == ["helper", "--option"]


@parametrize_with_cases("command", filter=id_has_suffix("_with_args"))
def test_ensure_list_with_more_args(command):
    assert _ensure_list(command) == ["helper", "--option", "arg"]
