from pathlib import Path

import pytest

from helper_auth import _ensure_list


@pytest.mark.parametrize(
    "command, expected",
    (
        pytest.param("helper", ["helper"], id="str"),
        pytest.param("helper --arg", ["helper", "--arg"], id="str with arg"),
        pytest.param(["helper"], ["helper"], id="list"),
        pytest.param(["helper", "--arg"], ["helper", "--arg"], id="list with arg"),
        pytest.param(Path("/etc/helper"), ["/etc/helper"], id="path-like"),
    ),
)
def test_ensure_list(command, expected):
    assert _ensure_list(command) == expected
