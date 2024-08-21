#!/usr/bin/python3

import os
import time
import threading
from argparse import ArgumentParser
from tqdm import tqdm #  python3 -m pip install tqdm
import datetime
from enum import IntEnum

# ./fileload.py --filesize 1048576 --iotype 2 --dst /cloud/nfs1/ --files 10 --threads 70 --sustain --timeout 6000
# ./fileload.py --filesize 5120 --iotype 2 --dst /cloud/nfs1/ --files 10 --threads 10
# ./fileload.py --filesize 5120 --iotype 2 --dst /cloud/nfs1/ --files 10 --threads 10 --sustain --timeout 6000
# ./fileload.py --filesize 1048576 --iotype 2 --dst /mnt/fun2 --files 10 --threads 10 --sustain --timeout 6000



alive = True

g_file_count = 100
g_thread_count = 5
g_byte_size = 1024

g_file_load_thread_object_list = []

class IoType(IntEnum):
    ZERO = 0
    RAND = 1
    SRAND = 2
class FileLoadJobParameters:
    def __init__(self):
        self.file_size_kb = 0
        self.io_type = 0
        self.destination = ""
        self.io_byte_size = g_byte_size
        self.file_count = g_file_count
        self.thread_count = g_thread_count
        self.sustain = False
        self.timeout = 0

def write_file(iFileName, iFileSize, iBlockSize, iIOType= IoType.ZERO, fsync=True):
    """
    Create a new file and fill it with zeros.

    Inputs:
        iFileName      (str): File
        iFileSize      (int): File size in KB
        iBlockSize     (int): Block size in KB
        fsync (bool): Fsync after IO is complete
    Outputs:
        NULL
    """
    buf = None
    if iIOType == IoType.ZERO:
        buf = '\0' * 1024
    elif iIOType == IoType.RAND:
        buf = os.urandom(iBlockSize)

    try:
        fh = os.open(iFileName, os.O_CREAT | os.O_TRUNC | os.O_WRONLY)
        while alive:
            if iIOType == IoType.SRAND:
                buf = os.urandom(iBlockSize)
            if iFileSize < iBlockSize:
                os.write(fh, buf * iFileSize)
                break
            os.write(fh, buf * iBlockSize)
            iFileSize -= iBlockSize
        # Force write of fdst to disk.
        if fsync:
            os.fsync(fh)
    except:
        raise
    finally:
        os.close(fh)


def generate_files(thread_id, iFileSizeKB, iIOType, bs=1024, dst=None, files=5000, sustain=False, timeout=0):
    """
    Generate files.

    Inputs:
        iFileSizeKB (int): file size
        qty    (int): Total file count
        iIOType  (int): File type
        dst    (str): Destination directory
        files  (int): File per directory
    Outputs:
        NULL
    """
    # Use current directory if not defined
    if not dst:
        dst = os.getcwd()

    if not os.path.isdir(dst):
        os.mkdir(dst)

    size = iFileSizeKB
    start_time = datetime.datetime.now()
    pbar = tqdm(total=files*size*1024, position=thread_id, unit='B', unit_scale=True, unit_divisor=1024)
    iteration = 0
    while True:

        current_ct = 0

        while current_ct < files:
            pbar.set_description(f"thread:{str(thread_id)} file:{current_ct}-{files} iter:{iteration}", refresh=True)
            if not alive:
                return

            # Write file.
            digits = len(str(files))
            basename = str(current_ct).zfill(digits)
            f = os.path.join(dst, ".".join([basename, "data"]))
            write_file(f, size, bs, iIOType)

            # Update counters.
            pbar.update(size*1024)
            current_ct += 1

        now_time = datetime.datetime.now().timestamp()
        if  (sustain == False) or (timeout != 0 and now_time > start_time.timestamp() + timeout):
            # pbar.close()
            # print("break because startnow_time:{}> start_time.timestamp():{} + timeout:{}".format(now_time, start_time.timestamp(), timeout))
            break

        iteration = iteration + 1

        pbar.reset()

def generate_file_load_threads(file_load_job_parameters):
    print("Starting Threads:{}".format(file_load_job_parameters.thread_count))
    thrs = []

    start = datetime.datetime.now()
    for i in range(file_load_job_parameters.thread_count):
        directory = file_load_job_parameters.destination + "/thread-" + str(i)

        t = threading.Thread(target=generate_files, args=(i,
                                                   file_load_job_parameters.file_size_kb,
                                                   file_load_job_parameters.io_type,
                                                   file_load_job_parameters.io_byte_size,
                                                   directory,
                                                   file_load_job_parameters.file_count,
                                                   file_load_job_parameters.sustain,
                                                   file_load_job_parameters.timeout))
        thrs.append(t)
        t.start()

    time.sleep(2)

    # Join threads, waiting for them to complete
    for t in thrs:
        t.join()

    done = datetime.datetime.now()

    # Let output finish...
    time.sleep(2)

    #print("\nStart:" + str(start))
    #print("Finished:" + str(done))
    #print("Difference:"  + str(done-start))

def main():
    # Define CLI arguments.
    parser = ArgumentParser(description='File generation utility.')
    parser.add_argument('--filesize', type=int, required=True,
                        help='file size in KiB')
    parser.add_argument('--iotype', '-f', dest='iotype', type=int, required=False, choices=list(map(int, IoType)),
                        default=IoType.RAND, help='io type')
    parser.add_argument('--dst', dest='dst', type=str, required=False,
                        help='destination directory')
    parser.add_argument('--files', dest='fcount', type=int, required=False,
                        default=20, help='files per thread')
    parser.add_argument('--bs', dest='bs', type=int, required=False,
                        default=1024, help='IO record size in bytes')
    parser.add_argument('--threads', dest="threads", type=int, required=False,
                        default=g_thread_count, help='thread count')
    parser.add_argument('--sustain', action='store_true', default=False, required=False,
                        help='should writes be sustained')
    parser.add_argument('--timeout', dest="timeout", type=int, required=False,
                        default=0, help='timeout of writes')

    args = parser.parse_args()

    fljp = FileLoadJobParameters
    fljp.file_size_kb = args.filesize
    fljp.io_type = args.iotype
    fljp.destination = args.dst
    fljp.file_count = args.fcount
    fljp.io_byte_size = args.bs
    fljp.thread_count = args.threads
    fljp.sustain = args.sustain
    fljp.timeout = args.timeout

    print("Arguments to file load job:" + str(fljp))
    generate_file_load_threads(fljp)

if __name__ == '__main__':
    main()
