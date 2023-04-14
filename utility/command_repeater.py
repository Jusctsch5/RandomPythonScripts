#!/bin/python3

import subprocess
import time
import argparse
import datetime


# Example:
# ~/my_scripts/command_repeater.py -c "smokeit -i -t cluster-brian1.ep.lab.atavium.com -c client-john-1.ep.lab.atavium.com jaws-qa -Case Controller-RestartIo" -i 1

if __name__ == "__main__":

    descriptionString = "Runs commands over and over. Will always wait for command to finish before starting another"
    parser = argparse.ArgumentParser(description=descriptionString)

    # Define Manditory Arguments.

    # Define Optional Arguments
    run_group = parser.add_mutually_exclusive_group(required=True)
    run_group.add_argument("-c", "--command", help="- command to run")
    run_group.add_argument("-s", "--script",  help="- script to run")

    parser.add_argument("-i", "--interval-seconds", type=int, default=1, help="- seconds between the script will run")
    parser.add_argument("-r", "--repeat", type=int, default=-1, help="- how many times to repeat (default: forever=-1)")
    parser.add_argument("-d", "--displaystdout", action='store_true', default=True, help="- display standard out from script")
    parser.add_argument("-o", "--outputfile", help="- capture standard output in file")

    # Populate Arguments
    args = parser.parse_args()

    repeat_counter = args.repeat
    while repeat_counter > 0 or args.repeat == -1:
        time_start = datetime.datetime.now()
        print("-------------------------------------------------")
        print("{} Start - Running iteration={} of script.".format(time_start, args.repeat - repeat_counter + 1))
        print("-------------------------------------------------")

        # process = subprocess.Popen([args.command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if args.displaystdout:
            process = subprocess.Popen(args.command, shell=True)

            # wait for the process to terminate
            out, err = process.communicate()
            errcode = process.returncode

            # print (subprocess.check_output(args.command, shell=True))
        else:
            subprocess.check_output(args.command, shell=True)

        repeat_counter = repeat_counter - 1
        time_end = datetime.datetime.now()
        print("-------------------------------------------------")
        print("{} End - Finished occurance={} of script. Diff={}".format(time_end, args.repeat - repeat_counter + 1, time_end - time_start))
        print("-------------------------------------------------")
        if args.interval_seconds:
            time.sleep(args.interval_seconds)