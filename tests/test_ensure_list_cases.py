from pathlib import Path


def case_str():
    return "helper"


def case_str_with_arg():
    return "helper --option"


def case_str_with_args():
    return "helper --option arg"


def case_list():
    return ["helper"]


def case_list_with_arg():
    return ["helper", "--option"]


def case_list_with_args():
    return ["helper", "--option", "arg"]


def case_path_like():
    return Path("helper")
