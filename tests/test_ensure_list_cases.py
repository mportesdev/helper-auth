from collections import namedtuple
from pathlib import Path

_case = namedtuple("_case", "command args expected")


def case_simple_string():
    return _case(
        command="helper",
        args=(),
        expected=["helper"],
    )


def case_simple_path_like():
    return _case(
        command=Path("helper"),
        args=(),
        expected=["helper"],
    )


def case_single_string_one_arg():
    return _case(
        command="helper --option",
        args=(),
        expected=["helper", "--option"],
    )


def case_single_string_more_args():
    return _case(
        command="helper --option arg",
        args=(),
        expected=["helper", "--option", "arg"],
    )


def case_separate_string_one_arg():
    return _case(
        command="helper",
        args=("--option",),
        expected=["helper", "--option"],
    )


def case_separate_string_more_args():
    return _case(
        command="helper",
        args=("--option", "arg"),
        expected=["helper", "--option", "arg"],
    )


def case_separate_path_like_one_arg():
    return _case(
        command=Path("helper"),
        args=("--option",),
        expected=["helper", "--option"],
    )


def case_separate_path_like_more_args():
    return _case(
        command=Path("helper"),
        args=("--option", "arg"),
        expected=["helper", "--option", "arg"],
    )
