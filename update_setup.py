#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Introduce : Generates a requirements.txt from current venv state and update setup.py
@File      : update_setup.py
@Project   : pygletPlayground
@Time      : 08.07.22 16:13
@Author    : flowmeadow
"""
import os


def main():
    os.system("pip freeze > requirements.txt")
    requirements = [i.strip() for i in open("requirements.txt").readlines()]

    with open("setup.py", "r") as f:
        lines = f.readlines()
        for l_idx, line in enumerate(lines):
            c_idx = line.find("install_requires")
            if c_idx > 0:
                lines[l_idx] = f"\tinstall_requires={requirements},\n"

    with open("setup.py", "w") as f:
        f.writelines(lines)


if __name__ == "__main__":
    main()
