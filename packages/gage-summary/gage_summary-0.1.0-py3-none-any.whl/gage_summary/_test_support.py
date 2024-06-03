# SPDX-License-Identifier: Apache-2.0

import os
import tempfile

from gage_summary import _compare_paths as compare_paths

__all__ = [
    "cat",
    "cd",
    "compare_paths",
    "ls",
    "os",
    "make_temp_dir",
]


def cd(s: str):
    os.chdir(os.path.expandvars(s))


def make_temp_dir(prefix: str = "gage-test-"):
    return tempfile.mkdtemp(prefix=prefix)


def ls(dirname: str = "."):
    names = sorted(os.listdir(dirname))
    if not names:
        print("<empty>")
    for name in names:
        print(name)


def cat(*parts: str):
    with open(os.path.join(*parts), "r") as f:
        s = f.read()
        if not s:
            print("<empty>")
        else:
            if s[-1:] == "\n":
                s = s[:-1]
            print(s)
