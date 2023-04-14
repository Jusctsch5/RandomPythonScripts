#!/usr/bin/python3
import argparse
import subprocess

def write_file(directory, id, size_mb):

    """
    Example:
    dd if=/dev/urandom of=/mnt/scale/testFile0 bs=10M count=1
    """
    command = "dd if=/dev/urandom of=$DIR/testFile$ID bs=$SIZEM count=1"
    command = command.replace("$DIR", directory)
    command = command.replace("$ID", str(id))
    command = command.replace("$SIZE", str(size_mb))
    print("Running command:\n" + command)

    # Run then wait for the process to terminate
    process = subprocess.Popen(command, shell=True)
    out, err = process.communicate()
    errcode = process.returncode

    print(out)        
    print(errcode)        

if __name__ == "__main__":
    
    descriptionString = "Writes files with random content"
    parser = argparse.ArgumentParser(description=descriptionString)

    parser.add_argument("-n", "--number", type=int, default=10, help="Number of files to write (default 10)")
    parser.add_argument("-s", "--sizeMB", type=int,  default=10, help="Size of files to write in MB (default 10 MB)")
    parser.add_argument("-d", "--directory", default="fun", help="Directory to generate files on")

    args = parser.parse_args()

    for i in range(args.number):
        write_file(args.directory, i, args.sizeMB)
