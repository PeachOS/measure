from psutil import Process, pid_exists
from subprocess import Popen
from sys import argv
from timeit import default_timer as timer
from time import sleep
from argparse import ArgumentParser, RawTextHelpFormatter
from math import floor
import methods

names = {"time": "time", "cpu": "cpu", ("mem", "r"): "rss", ("mem", "v"): "vms", ("mem", "e"): "num_page_faults",
         ("mem", "W"): "peak_wset", ("mem", "w"): "wset", ("mem", "P"): "peak_paged_pool", ("mem", "p"): "paged_pool",
         ("mem", "N"): "peak_nonpaged_pool", ("mem", "n"): "nonpaged_pool", ("mem", "f"): "pagefile",
         ("mem", "F"): "peak_pagefile", ("mem", "x"): "private", ("mem", "u"): "uss", ("io", "R"): "read_count",
         ("io", "r"): "read_bytes", ("io", "W"): "write_count", ("io", "w"): "write_bytes", ("io", "O"): "other_count", ("io", "o"): "other_bytes"}


def main(argv):
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)

    parser.add_argument("path_to_executable")

    parser.add_argument("-time", default="500", help="""Time interval in ms.
    Minimum value: 50 (set to 50 if below)
    The interval is not perfectly met. Tried my best. Observing +/-10ms
Example usage: -time 500 (default)""")

    parser.add_argument("--cpu", action='store_true', help="""Flag that activates cpu measurement.""")

    parser.add_argument("-mem", default="rWx", help="""Concatenate any of the following chars:
    r (Resident set size)
    v (Virtual memory size)
    e (Number of page faults)
    w (Working set),\tW (Peak working set)
    p (Paged pool),\tP (Peak paged pool)
    n (Non paged pool),N (Peak Non paged pool)
    f (Page file),\tF (Peak page file)
    x (private)
    u (Unique set size)
Example usage: -mem rWx (default)""")

    parser.add_argument("-io", default="wr", help="""Concatenate any of the following chars:
    r (Read bytes),\tR (Read count)
    w (Write bytes),\tW (Write count)
    o (Other bytes),\tO (Other count)
Example usage: -io wr (default)""")

    args = parser.parse_args()

    execute_path = args.path_to_executable

    proc = Popen(execute_path)

    pid = proc.pid

    watch(pid, args)


def watch(pid: int, args):
    print("watching pid " + str(pid))
    start_time = timer()
    process = Process(pid)
    process.cpu_percent(interval=None)
    time_sec = int(args.time) / 1000.0
    c = 0
    while pid_exists(pid):
        c += 1
        loop_a_time = timer() - start_time

        stat = ""

        snap = {}

        snap["time"] = floor(loop_a_time * 1000)


        ############################
        # CPU
        ############################

        cpu = process.cpu_percent(interval=None)

        ############################
        # Memory
        ############################

        mem = process.memory_full_info()

        ############################
        # I/O
        ############################

        io = process.io_counters()

        ############################
        # Snap
        ############################

        if (args.cpu):
            snap["cpu"] = cpu

        if args.mem.find('r') >= 0:
            snap[("mem", "r")] = mem.rss
        if args.mem.find('v') >= 0:
            snap[("mem", "v")] = mem.vms
        if args.mem.find('e') >= 0:
            snap[("mem", "e")] = mem.num_page_faults
        if args.mem.find('W') >= 0:
            snap[("mem", "W")] = mem.peak_wset
        if args.mem.find('w') >= 0:
            snap[("mem", "w")] = mem.wset
        if args.mem.find('P') >= 0:
            snap[("mem", "P")] = mem.peak_paged_pool
        if args.mem.find('p') >= 0:
            snap[("mem", "p")] = mem.paged_pool
        if args.mem.find('N') >= 0:
            snap[("mem", "N")] = mem.peak_nonpaged_pool
        if args.mem.find('n') >= 0:
            snap[("mem", "n")] = mem.nonpaged_pool
        if args.mem.find('f') >= 0:
            snap[("mem", "f")] = mem.pagefile
        if args.mem.find('F') >= 0:
            snap[("mem", "F")] = mem.peak_pagefile
        if args.mem.find('x') >= 0:
            snap[("mem", "x")] = mem.private
        if args.mem.find('u') >= 0:
            snap[("mem", "u")] = mem.uss

        if args.io.find('R') >= 0:
            snap[("io", "R")] = io.read_count
        if args.io.find('r') >= 0:
            snap[("io", "r")] = io.read_bytes
        if args.io.find('W') >= 0:
            snap[("io", "W")] = io.write_count
        if args.io.find('w') >= 0:
            snap[("io", "w")] = io.write_bytes
        if args.io.find('O') >= 0:
            snap[("io", "O")] = io.other_count
        if args.io.find('o') >= 0:
            snap[("io", "o")] = io.other_bytes


        if c == 1:
            methods.PrintAtEndMethod.init(list(snap.keys()))

        methods.PrintAtEndMethod.step(snap)

        # print(stat)

        loop_z_time = (timer() - start_time - loop_a_time)
        # print("duration: " + str((loop_z_time*1000)))
        # print("sleep for " + str((int(args.time) / 1000.0 - loop_z_time)*1000))
        sleep(time_sec - loop_z_time)
    print()
    methods.PrintAtEndMethod.finalize()


if __name__ == '__main__':
    main(argv)
