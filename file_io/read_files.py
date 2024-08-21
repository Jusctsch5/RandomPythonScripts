#!/usr/bin/python3

import os
import time
import threading
from random import randint
from argparse import ArgumentParser
from tqdm import tqdm #  python3 -m pip install tqdm
import glob
import math
import subprocess

g_thread_count = 5
g_kbyte_size = 1024

g_bytes_read = 0
g_files_read = 0
g_alive = True

class FileReadJobParameters:
    def __init__(self):
        self.read_size_kbyte = g_kbyte_size
        self.duration = 0
        self.sustain = False
        self.files_to_read = 0
        self.thread_count = g_thread_count
        self.source = ""

# Maybe this shouldn't be done so much,
# but I'm concerned that caching will come into play
# when rereading the same files
def drop_caches():
    command = 'echo 3 > /proc/sys/vm/drop_caches'
    process = subprocess.Popen(command, shell=True)
    out, err = process.communicate()
    errcode = process.returncode

def read_file(test_file, read_size_kb):
    size = os.path.getsize(test_file)
    read_size = read_size_kb * 1024
    running_size = 0
    with open(test_file, "rb") as fd:
        chunk = fd.read(read_size)
        running_size += len(chunk)
        while chunk:
            chunk = fd.read(read_size)
            running_size += len(chunk)

    global g_files_read
    g_files_read += 1
    global g_bytes_read
    g_bytes_read += running_size
    return running_size

def fileread(thread_id, files, read_size_kb, repeat):
    total_size = 0
    for file in files:
        total_size += os.path.getsize(file)

    pbar = tqdm(total=total_size, position=thread_id, unit='B', unit_scale=True, unit_divisor=1024)

    while 1:
        pbar.set_description("thread-"+str(thread_id), refresh=True)

        for test_file in files:
            bytes_read = read_file(test_file, read_size_kb)
            pbar.update(bytes_read)

        if repeat == False:
            return
        if g_alive == False:
            return

        bytes_read = 0
        pbar.reset()
        drop_caches() # blargh

def divide_chunks(file_list, n):
    chunks = [file_list[x:x+n] for x in range(0, len(file_list), n)]
    return chunks

def read_files(frjp):
    drop_caches()
    thrs = []
    dest = frjp.source
    result = [y for x in os.walk(dest) for y in glob.glob(os.path.join(x[0], '*.data'))]

    # For reading controlled number of files
    if frjp.files_to_read != 0:
        result = result[0:frjp.files_to_read]

    total_files = len(result)
    files_per_thread = math.ceil(total_files / frjp.thread_count)
    chunks = divide_chunks(result, files_per_thread)

    for i in range(frjp.thread_count):
        if i >= len(chunks):
            break

        print("Starting thread {} with ownership of {} files".format(i, len(chunks[i])))
        t = threading.Thread(target=fileread, args=(i, 
                             chunks[i],
                             frjp.read_size_kbyte, 
                             frjp.sustain))
        thrs.append(t)
        t.start()

    time.sleep(frjp.duration)        
    global g_alive
    g_alive = False
    # Join threads
    for t in thrs:
        t.join()

def main():
    # Define CLI arguments.
    parser = ArgumentParser(description='File read utility.')

    parser.add_argument('--src', dest='src', type=str, required=True,
                        default=None, help='source directory')    
    parser.add_argument('--files', dest='files', type=int, 
                        default=0, help='files to read, 0 for no limit')
    parser.add_argument('--bs', dest='bs', type=int, required=False,
                        default=1024, help='IO record size')
    parser.add_argument('--threads', dest="threads", type=int, required=False,
                        default=g_thread_count, help='thread count')
    parser.add_argument('--sustain', action='store_true', default=False, required=False,
                        help='should reads be sustained')                        
    parser.add_argument('--timeout', dest='timeout', type=int, 
                        default=0, help='timeout to read, 0 for single sweep')                        
    args = parser.parse_args()

    frjp = FileReadJobParameters
    frjp.read_size_kbyte = args.bs
    frjp.duration = args.timeout
    frjp.sustain = args.sustain
    frjp.files_to_read = args.files
    frjp.thread_count = args.threads
    frjp.source = args.src

    read_files(frjp)

if __name__ == '__main__':
    main()
