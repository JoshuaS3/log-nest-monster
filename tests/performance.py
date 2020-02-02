#!/usr/bin/env python3.7
"""Compiles tests/header_only.c to test size, tests/header_unit*.c to test speed"""

import sys
import os
import subprocess
import re
from statistics import median

PROJECT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
)
BIN_PATH = os.path.join(PROJECT_PATH, "bin")
INCLUDE_PATH = os.path.join(PROJECT_PATH, "src/c")
HEADER_ONLY = os.path.join(PROJECT_PATH, "tests/header_only.c")
HEADER_MAIN = os.path.join(PROJECT_PATH, "tests/header_unit.c")
HEADER_MAIN_2 = os.path.join(PROJECT_PATH, "tests/header_unit_2.c")

CC = "gcc"
CFLAGS = ["-pedantic", "-Wall", "-Wextra", "-Werror"]
COUTFLAG = "-o"
COPTIMIZATIONS = ["-O0", "-O1", "-O2", "-O3", "-Os"]
CINCLUDES = ["-I", INCLUDE_PATH]

TABLE_HEADER_1 = "Optimization Level"
TABLE_HEADER_2 = "Header Binary Size (in bytes)"
TABLE_HEADER_3 = "Unit Test Runtime (in µs)"

RE_TRIAL_TIME = r"time elapsed \(us\): (\d*)"


def gcc_compile(out_file: str, in_files: list, optimization_level: str = "-O0"):
    """Uses gcc subprocess to compile at a set optimization level"""
    process_command = (
        [CC]
        + CFLAGS
        + CINCLUDES
        + [COUTFLAG, out_file]
        + in_files
        + [optimization_level]
    )
    process = subprocess.run(process_command, stdout=sys.stdout, stderr=sys.stderr)
    if process.returncode:
        print("gcc_compile: error in compilation")
        return 0
    return 1


def execute_file(executable: str):
    """Executes the input file and returns the stdout"""
    process = subprocess.run([executable], capture_output=True, text=True)
    return process.stdout


def get_size(file_name: str):
    """Uses os.stat to get the file size in bytes of a specified file"""
    return os.stat(file_name).st_size


if __name__ == "__main__":
    try:
        os.mkdir(BIN_PATH)
    except FileExistsError:
        pass
    print("running compiler")
    for optimization in COPTIMIZATIONS:
        header_only_out = os.path.join(BIN_PATH, f"header_only{optimization}")
        if not gcc_compile(header_only_out, [HEADER_ONLY], optimization):
            sys.exit()
        header_unit_out = os.path.join(BIN_PATH, f"c{optimization}")
        if not gcc_compile(header_unit_out, [HEADER_MAIN, HEADER_MAIN_2], optimization):
            sys.exit()
    print("getting results")
    EXECUTABLE_SIZES = {}
    EXECUTABLE_RUNTIMES = {}
    for optimization in COPTIMIZATIONS:
        header_only_out = os.path.join(BIN_PATH, f"header_only{optimization}")
        header_unit_out = os.path.join(BIN_PATH, f"c{optimization}")
        EXECUTABLE_SIZES[optimization] = get_size(header_only_out)
        trial_runtimes = []
        for trial_num in range(200):
            trial_output = execute_file(header_unit_out)
            trial_time = re.search(RE_TRIAL_TIME, trial_output).group(1)
            trial_runtimes.append(int(trial_time))
        EXECUTABLE_RUNTIMES[optimization] = int(median(trial_runtimes))
    print("done. printing...")
    print()
    print(f"{TABLE_HEADER_1} | {TABLE_HEADER_2} | {TABLE_HEADER_3}")
    print(
        f"{len(TABLE_HEADER_1)*'-'} | {len(TABLE_HEADER_2)*'-'} | {len(TABLE_HEADER_3)*'-'}"
    )
    for optimization in COPTIMIZATIONS:
        executable_size = EXECUTABLE_SIZES[optimization]
        executable_runtime = EXECUTABLE_RUNTIMES[optimization]
        print(
            f"{optimization.ljust(len(TABLE_HEADER_1))} | "
            + f"{str(executable_size).ljust(len(TABLE_HEADER_2))} | {executable_runtime}"
        )
