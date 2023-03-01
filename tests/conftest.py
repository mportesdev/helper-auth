try:
    import tomllib
except ModuleNotFoundError:
    collect_ignore = ["test_version.py"]
