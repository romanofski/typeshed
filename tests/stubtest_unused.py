#!/usr/bin/env python3

# Runs stubtest and prints each unused whitelist entry with filename.

from typing import List, Tuple
import os.path
import subprocess
import sys

_UNUSED_NOTE = "note: unused whitelist entry "
_WHITELIST_PATH = os.path.join("tests", "stubtest_whitelists")


def main() -> int:
    unused = run_stubtest()
    with_filenames = []
    for uu in unused:
        with_filenames.extend(unused_files(uu))
    for file, uu in with_filenames:
        print(file + ":" + uu)
    return 1 if with_filenames else 0


def run_stubtest() -> List[str]:
    popen = subprocess.Popen(
        ["./tests/stubtest_test.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
    )
    assert popen.stdout is not None
    unused = []
    for line in popen.stdout:
        if line.startswith(_UNUSED_NOTE):
            unused.append(line[len(_UNUSED_NOTE):].strip())
    popen.wait()
    return unused


def unused_files(unused: str) -> List[Tuple[str, str]]:
    version = "py{}{}".format(sys.version_info[0], sys.version_info[1])
    files = ["py3_common.txt", version + ".txt", sys.platform + ".txt", sys.platform + "-" + version + ".txt"]
    found = []
    for file in files:
        path = os.path.join(_WHITELIST_PATH, file)
        if find_unused_in_file(unused, path):
            found.append((path, unused))
    if not found:
        raise ValueError("unused item {} not found in any whitelist file".format(unused))
    return found


def find_unused_in_file(unused: str, path: str) -> bool:
    try:
        with open(path) as f:
            return any(line.strip().split(" ")[0] == unused for line in f)
    except FileNotFoundError:
        return False


if __name__ == "__main__":
    sys.exit(main())
