import tomllib

import helper_auth


def test_version_info_matches_metadata():
    with open("pyproject.toml", "rb") as f:
        metadata = tomllib.load(f)["tool"]["poetry"]

    assert helper_auth.__version__ == metadata["version"]
