import sys

if sys.version_info < (3, 11):
    collect_ignore = ["test_version.py"]
