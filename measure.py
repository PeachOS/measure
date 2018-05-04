from psutil import Process, pid_exists
from subprocess import Popen
from sys import argv
from timeit import default_timer as timer
from time import sleep
from argparse import ArgumentParser, RawTextHelpFormatter
from math import floor


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

    print(header_line(args))

    while pid_exists(pid):
        loop_a_time = timer() - start_time

        stat = ""

        stat += str(floor(loop_a_time * 1000))

        ############################
        # CPU
        ############################

        cpu = process.cpu_percent(interval=None)
        if (args.cpu):
            stat += "\t" + str(cpu)

        loop_b_time = timer() - start_time

        ############################
        # Memory
        ############################

        mem = process.memory_full_info()

        if args.mem.find('r') >= 0:
            stat += "\t" + str(mem.rss)
        if args.mem.find('v') >= 0:
            stat += "\t" + str(mem.vms)
        if args.mem.find('e') >= 0:
            stat += "\t" + str(mem.num_page_faults)
        if args.mem.find('W') >= 0:
            stat += "\t" + str(mem.peak_wset)
        if args.mem.find('w') >= 0:
            stat += "\t" + str(mem.wset)
        if args.mem.find('P') >= 0:
            stat += "\t" + str(mem.peak_paged_pool)
        if args.mem.find('p') >= 0:
            stat += "\t" + str(mem.paged_pool)
        if args.mem.find('N') >= 0:
            stat += "\t" + str(mem.peak_nonpaged_pool)
        if args.mem.find('n') >= 0:
            stat += "\t" + str(mem.nonpaged_pool)
        if args.mem.find('f') >= 0:
            stat += "\t" + str(mem.pagefile)
        if args.mem.find('F') >= 0:
            stat += "\t" + str(mem.peak_pagefile)
        if args.mem.find('x') >= 0:
            stat += "\t" + str(mem.private)
        if args.mem.find('u') >= 0:
            stat += "\t" + str(mem.uss)

        loop_c_time = timer() - start_time

        ############################
        # I/O
        ############################

        io = process.io_counters()

        if args.io.find('R') >= 0:
            stat += "\t" + str(io.read_count)
        if args.io.find('r') >= 0:
            stat += "\t" + str(io.read_bytes)
        if args.io.find('W') >= 0:
            stat += "\t" + str(io.write_count)
        if args.io.find('w') >= 0:
            stat += "\t" + str(io.write_bytes)
        if args.io.find('O') >= 0:
            stat += "\t" + str(io.other_count)
        if args.io.find('o') >= 0:
            stat += "\t" + str(io.other_bytes)


        print(stat)

        loop_z_time = (timer() - start_time - loop_a_time)
        sleep(int(args.time)/1000.0 - loop_z_time)


def header_line(args):
    stat = "time"

    if args.cpu:
        stat += "\t cpu"

    if args.mem.find('r') >= 0:
        stat += "\t rss"
    if args.mem.find('v') >= 0:
        stat += "\t vms"
    if args.mem.find('e') >= 0:
        stat += "\t num_page_faults"
    if args.mem.find('W') >= 0:
        stat += "\t peak_wset"
    if args.mem.find('w') >= 0:
        stat += "\t wset"
    if args.mem.find('P') >= 0:
        stat += "\t peak_paged_pool"
    if args.mem.find('p') >= 0:
        stat += "\t paged_pool"
    if args.mem.find('N') >= 0:
        stat += "\t peak_nonpaged_pool"
    if args.mem.find('n') >= 0:
        stat += "\t nonpaged_pool"
    if args.mem.find('f') >= 0:
        stat += "\t pagefile"
    if args.mem.find('F') >= 0:
        stat += "\t peak_pagefile"
    if args.mem.find('x') >= 0:
        stat += "\t private"
    if args.mem.find('u') >= 0:
        stat += "\t uss"
    if args.io.find('R') >= 0:
        stat += "\tread_count"
    if args.io.find('r') >= 0:
        stat += "\tread_bytes"
    if args.io.find('W') >= 0:
        stat += "\twrite_count"
    if args.io.find('w') >= 0:
        stat += "\twrite_bytes"
    if args.io.find('O') >= 0:
        stat += "\tother_count"
    if args.io.find('o') >= 0:
        stat += "\tother_bytes"

    return stat

if __name__ == '__main__':
    main(argv)
