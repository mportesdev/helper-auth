from pytest_cases import parametrize_with_cases

from helper_auth import _ensure_list


@parametrize_with_cases("case")
def test_ensure_list(case):
    assert _ensure_list(*case.command) == case.expected
