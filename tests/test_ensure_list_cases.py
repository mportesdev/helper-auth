from pathlib import Path


def case_simple_string():
    return ("helper",)


def case_simple_path_like():
    return (Path("helper"),)


def case_single_string_one_arg():
    return ("helper --option",)


def case_single_string_more_args():
    return ("helper --option arg",)


def case_separate_string_one_arg():
    return "helper", "--option"


def case_separate_string_more_args():
    return "helper", "--option", "arg"


def case_separate_path_like_one_arg():
    return Path("helper"), "--option"


def case_separate_path_like_more_args():
    return Path("helper"), "--option", "arg"
