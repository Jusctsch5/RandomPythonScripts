#!/usr/bin/env python3
import os
import random
import string
import subprocess
import argparse
letters = string.ascii_letters

def Main():
    # Define CLI arguments.
    parser = argparse.ArgumentParser(description='Create a file using large range, then create more nuggets by splitting the range.')
    parser.add_argument('--output', '-o', type=str, required=True,help='directory to genrate files')
    parser.add_argument('--directories', '-d', type=int, required=True, help='Number of directories to generate')
    parser.add_argument('--files', '-f', type=int, required=True, help='Number of files to generate')

    args = parser.parse_args()

    for i in range(args.number):
        random_dir_name = args.directory.join(random.choice(letters) for _ in range(10))
        if not os.path.exists(random_dir_name):
            os.mkdir(random_dir_name)
        os.chdir(random_dir_name)
        n = 1
        for j in range(args.files):
            random_file_name = ''.join(random.choice(letters) for _ in range(10))
            subprocess.call(['touch', random_file_name + ".txt"])
        os.chdir("..")


Main()