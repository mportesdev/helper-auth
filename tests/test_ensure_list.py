from pytest_cases import parametrize_with_cases

from helper_auth import _ensure_list


@parametrize_with_cases("command")
def test_ensure_list(command, current_cases):
    if "with_arg" in current_cases["command"].id:
        assert _ensure_list(command) == ["helper", "--option"]
    else:
        assert _ensure_list(command) == ["helper"]
