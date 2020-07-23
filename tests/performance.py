#!/usr/bin/env python3
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
HEADER_PERFORMANCE = os.path.join(PROJECT_PATH, "tests/header_memory.c")

CC = "gcc"
CFLAGS = ["-std=c11", "-pedantic", "-Wall", "-Wextra", "-Werror"]
COUTFLAG = "-o"
COPTIMIZATIONS = ["-O0", "-O1", "-O2", "-O3", "-Os"]
CINCLUDES = ["-I", INCLUDE_PATH]

TABLE_HEADER_1 = "Optimization Level"
TABLE_HEADER_2 = "Header Binary Size (in bytes)"
TABLE_HEADER_3 = "Memory Test Runtime (in µs)"

RE_TRIAL_TIME = r"time elapsed \(us\): (\d*)"
TRIAL_PASSES = 200


def cc_compile(out_file: str, in_files: list, optimization_level: str = "-O0"):
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
        print("[cc_compile] error in compilation")
        return 0
    else:
        print(f"[cc_compile] finished compiling to {out_file}")
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
    else:
        print("[main] created bin/")
    print("[main] compiling...")
    print(f"[main/compile] using compiler {CC}")
    for optimization in COPTIMIZATIONS:
        header_only_out = os.path.join(BIN_PATH, f"c-header-only{optimization}")
        if not cc_compile(header_only_out, [HEADER_ONLY], optimization):
            sys.exit()
        header_unit_out = os.path.join(BIN_PATH, f"c-performance{optimization}")
        if not cc_compile(header_unit_out, [HEADER_PERFORMANCE], optimization):
            sys.exit()
    print("[main] getting filesize data of header_only binaries")
    EXECUTABLE_SIZES = {}
    for optimization in COPTIMIZATIONS:
        header_only_out = os.path.join(BIN_PATH, f"c-header-only{optimization}")
        EXECUTABLE_SIZES[optimization] = get_size(header_only_out)
    print("[main] beginning time trials")
    EXECUTABLE_RUNTIMES = {}
    import matplotlib.pyplot as plt
    plt.xlabel("trial")
    plt.ylabel("time (µs)")
    for optimization in COPTIMIZATIONS:
        print(f"[main/trials] running trial on {optimization}")
        header_unit_out = os.path.join(BIN_PATH, f"c-performance{optimization}")
        trial_runtimes = []
        for trial_num in range(TRIAL_PASSES):
            trial_output = execute_file(header_unit_out)
            trial_time = re.search(RE_TRIAL_TIME, trial_output).group(1)
            trial_runtimes.append(int(trial_time))
        plt.plot(trial_runtimes)
        trial_runtimes.sort()
        trial_median = int(median(trial_runtimes))
        trial_mid = int(TRIAL_PASSES/2)
        trial_iqr = int(median(trial_runtimes[trial_mid:TRIAL_PASSES]) - median(trial_runtimes[0:trial_mid]))
        trial_moe = int(trial_iqr/2)
        EXECUTABLE_RUNTIMES[optimization] = f"{trial_median} ± {trial_moe}"
    plt.legend(COPTIMIZATIONS)
    print("[main] finished trials:")
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
    plt.show()
