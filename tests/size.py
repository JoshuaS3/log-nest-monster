#!/usr/bin/env python3.7
"""Compiles the base source for output speed and size tests using different optimization levels"""

import subprocess
import os

PROJECT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
)
HEADER_PATH = os.path.join(PROJECT_PATH, "src/c")
TEST_FILE = os.path.join(PROJECT_PATH, "tests/base_header.c")
OUT_FILE = os.path.join(PROJECT_PATH, "bin/performance")

CC = "gcc"
CFLAGS = ["-pedantic", "-Wall", "-Wextra", "-Werror"]
COUTFLAG = "-o"
COPTIMIZATIONS = ["-O0", "-O1", "-O2", "-O3", "-Os"]
CINCLUDES = ["-I", HEADER_PATH]


def gcc_compile(file_name: str, optimization_level: str = "-O0"):
    """Uses gcc subprocess to compile at a set optimization level"""
    process_command = (
        [CC] + CFLAGS + CINCLUDES + [COUTFLAG, file_name, TEST_FILE, optimization_level]
    )
    process = subprocess.Popen(process_command)
    process.wait()  # wait for execution
    if process.returncode:
        raise Exception(f"gcc_compile: error in compilation")


def get_size(file_name: str):
    """Uses os.stat to get the file size in bytes of a specified file"""
    return os.stat(file_name).st_size


if __name__ == "__main__":
    for optimization in COPTIMIZATIONS:
        out_file = f"{OUT_FILE}{optimization}"
        gcc_compile(out_file, optimization)
        print(f"Level {optimization}: {get_size(out_file)}")
