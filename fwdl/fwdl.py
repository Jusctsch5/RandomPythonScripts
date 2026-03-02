#!/usr/bin/env python3
import os, sys, binascii, subprocess, argparse
from time import sleep
from collections import OrderedDict
import logging
from datetime import datetime


logging.basicConfig(filename='fwdl.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

def error(msg):
    sys.stderr.write("Err: %s\n" % (msg,))
    sys.exit(1)

# --- - chunking helpers
def getchunks(seq, size):
    '''Generator that cuts sequence (bytes, memoryview, etc.)
     into chunks of given size. If `seq` length is not multiply
     of `size`, the lengh of the last chunk returned will be
     less than requested.

     >>> list( chunks([1,2,3,4,5,6,7], 3) )
     [[1, 2, 3], [4, 5, 6], [7]]
    '''
    d, m = divmod(len(seq), size)
    for i in range(d):
        yield seq[i*size:(i+1)*size]
    if m:
        yield seq[d*size:]

def dumphex(binary, size=2, sep=' '):
    '''
    Convert binary data (bytes in Python 3 and str in
    Python 2) to hex string like '00 DE AD BE EF'.
    `size` argument specifies length of text chunks
    and `sep` sets chunk separator.
    '''
    hexstr = binascii.hexlify(binary)
    if sys.version_info >= (3, 0):
      hexstr = hexstr.decode('ascii')
    chunks = getchunks(hexstr, size)
    pre_hex = ['0x' + h for h in chunks]
    count = len(pre_hex)
    #if count < 32:
    #  pre_hex.extend(["0xff"] * (32-count))
    #assert(len(pre_hex)==32)
    #return sep.join(pre_hex)
    return pre_hex

parser = argparse.ArgumentParser()
#parser.add_argument('-t', '--target',
#	help="Target Server Name/IP", default='192.168.100.1')
#parser.add_argument('-u', '--user',
#	help="IPMI User Name", default="ADMIN")
#parser.add_argument('-p', '--password',
#	help="IPMI Password", default="ADMIN")
parser.add_argument('-i', '--i2caddr',
	help="i2c address", default="0x38")
parser.add_argument('-f', '--file',
        help="FW binary file", default="./APROM_32K_R11.BIN")
args = parser.parse_args()
#print(args)

data_length = '0x3'
mux_channel = '0x0'
#i2c_addr = '0x38'
i2c_addr = args.i2caddr
i2c_addr_read = int(i2c_addr, 16) | 1

ipmi_cmd = ['ipmitool']
#ipmi_cmd.extend(['-I', 'lanplus'])
#ipmi_cmd.extend(['-H', args.target])
#ipmi_cmd.extend(['-U', args.user])
#ipmi_cmd.extend(['-P', args.password])
ipmi_cmd.extend(['raw', '0x30', '0xb6', '0x45', '0x63', '0x68', '0x6f', '0x43', '0x74', '0x72', '0x6c'])

def ipmi_setcmd():
    set_cmd = ipmi_cmd[:]
    set_cmd.extend(['0x0', '0x3', mux_channel, '0x3', i2c_addr, '0x50', hex(i2c_addr_read)])
    return set_cmd

def ipmi_readcmd():
    read_cmd = ipmi_cmd[:]
    read_cmd.extend(['0x0', '0x4'])
    return read_cmd

# hexlist: [16 bytes]
def ipmi_writecmd(offset, hexlist):
    write_cmd = ipmi_cmd[:]
    write_cmd.extend([ '0x1', '0x2', mux_channel, i2c_addr, '0x54', hex(offset & 0xff), hex(offset >> 8 & 0xff)])
    #write_cmd.extend(['0x0', '0x3', mux_channel, '0x0', i2c_addr, '0x54', hex(offset & 0xff), hex(offset >> 8 & 0xff)])
    #write_cmd.extend(['0x0', '0x3', mux_channel, data_length, i2c_addr, '0x54', hex(offset >> 8 & 0xff), hex(offset & 0xff)])
    write_cmd.extend(hexlist)
    return write_cmd

def ipmi_chunkcmd(offset):
    chunk_cmd = ipmi_cmd[:]
    chunk_cmd.extend(['0x0', '0x3', mux_channel, '0x10', i2c_addr, '0x55', hex(offset & 0xff), hex(offset >> 8 & 0xff)])
    return chunk_cmd

def ipmi_cmdrun(hexlist):
    run_cmd = ipmi_cmd[:]
    run_cmd.extend(['0x0', '0x3', mux_channel, '0x0', i2c_addr])
    run_cmd.extend(hexlist)
    #print run_cmd
    return run_cmd

def find_ipmitool():
    ret = False
    try:
        p = subprocess.Popen(['ipmitool', '-V'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        out, err = p.communicate()
        sys.stdout.write('Found %s' % out)
        ret = True
    except Exception:
        print("ipmitool not found.")
    return ret

def ipmitool_setchunk(offset):
    ret = False
    try:
        p = subprocess.Popen(ipmi_chunkcmd(offset), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        out, err = p.communicate()
        #print(err)
        #print(out)
        if len(err) == 0:
            ret = True
    except OSError as e:
        print ("OSError: %s" % e.strerror)
    except:
        print ("Error(ipmitool_setchunk): %s" % sys.exc_info()[0])

    return ret

def ipmitool_set():
    ret = False
    try:
        p = subprocess.Popen(ipmi_setcmd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        out, err = p.communicate()
        #print(err)
        #print(out)
        if len(err) == 0:
            ret = True
    except OSError as e:
        print ("OSError: %s" % e.strerror)
    except:
        print ("Error(ipmitool_set): %s" % sys.exc_info()[0])

    print("ipmitool_set: %s" % ret)
    print("ipmitool_set: %s" % out)
    print("ipmitool_set: %s" % err)

    return ret

def ipmitool_run(hexlist):
    ret = False
    try:
        p = subprocess.Popen(ipmi_cmdrun(hexlist), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        out, err = p.communicate()
        #print(err)
        #print(out)
        if len(err) == 0:
            ret = True
    except OSError as e:
        print ("OSError: %s" % e.strerror)
    except:
        print ("Error(ipmitool_run): %s" % sys.exc_info()[0])
    return ret

def run_appmode():
    print("Enter APP Mode...")
    ipmitool_run(['0x52', '0xA5', '0x5A'])

def run_blmode():
    print("Enter BL Mode...")
    ipmitool_run(['0x51', '0xB5', '0x5B'])

def erase_aprom():
    print("Erase APROM...")
    ipmitool_run(['0x53', '0xE5', '0x5E'])

def ipmitool_verify():
    ret = False
    try:
        p = subprocess.Popen(ipmi_readcmd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        out, err = p.communicate()
        data_hex = b''
        for line in out.splitlines():
            #logging.debug(line)
            data_hex += bytearray.fromhex(line.strip())

        #print data_hex[0]
        if data_hex[0] == 3:
            ret = True

    except OSError as e:
        print("OSError: %s" % e.strerror)
    except:
        print("Error(ipmitool_read): %s" % sys.exc_info()[0])

    return ret

def ipmitool_read():
    data_out = b''
    try:
        p = subprocess.Popen(ipmi_readcmd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        out, err = p.communicate()
        data_hex = b''
        for line in out.splitlines():
            #logging.debug(line)
            data_hex += bytearray.fromhex(line.strip())
        if data_hex[0] == 3:
            data_out = data_hex[1:]

    except OSError as e:
        print("OSError: %s" % e.strerror)
    except:
        print("Error(ipmitool_read): %s" % sys.exc_info()[0])

    return data_out

def ipmitool_write(offset, hexlist):
    try:
        #logging.debug("Writing 16 bytes (offset %d)" % offset)
        #logging.debug(hexlist)
        p = subprocess.Popen(ipmi_writecmd(offset, hexlist), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        out, err = p.communicate()
        #print(out)
    except OSError as e:
        print("OSError: %s" % e.strerror)
    except:
        print("Error: %s" % sys.exc_info()[0])

def read_status():
    if not ipmitool_set():
        sys.exit(1)
    sleep(1)
    mcu_data = ipmitool_read()
    if len(mcu_data) == 0:
        print("Unable to read MCU Info.")
        sys.exit(1)

    #logging.debug("Received %d bytes" % len(mcu_data))

    if mcu_data[0] == 0xA0:
        mode = "APP"
    else:
        mode = "BL"

    print("Mode: %s, Version: %d.%d, Status: %s" % (mode, mcu_data[1] >> 4, mcu_data[1] & 0xf, hex(mcu_data[2])))
    return mcu_data[0], mcu_data[2]

def read_chunk(offset):
    if not ipmitool_setchunk(offset):
        sys.exit(1)
    #sleep(0.5)
    while True:
        chunk = ipmitool_read()
        if len(chunk) == 16:
            break

    #print chunk
    return chunk

def check_file():
    file = open(args.file, "rb")
    bytes = file.read()
    checksum = 0
    for i in range(0, 0x7ffc):
        checksum += int(binascii.hexlify(bytes[i]), 16)

    #print checksum

    s1 = int(binascii.hexlify(bytes[0x7ffc]), 16)
    s2 = int(binascii.hexlify(bytes[0x7ffd]), 16) << 8
    s3 = int(binascii.hexlify(bytes[0x7ffe]), 16) << 16
    vsum = s1 + s2 + s3
    #print vsum
    if vsum == checksum:
        print("Verify Checksum... OK")
    else:
        print("Invalid Checksum")
        sys.exit(1)

    fmode = int(binascii.hexlify(bytes[0x7fff]), 16)
    if (fmode < 17 or fmode > 20):
        print("Invalid mode")
        sys.exit(1)

    file.close()

def compare_chunk(chunk, datachunk):
    for index in range(0, 16):
        if chunk[index] != int(binascii.hexlify(datachunk[index]),16):
            return False
    return True

###########################

if not find_ipmitool():
    sys.exit(1)

#print('IP: %s' % args.target)
print('Reading (MUX channel: %s, Addr: %s)...' % (mux_channel, i2c_addr))
read_status()

#status:
#(APP mode)
# 0xff
#(BL mode)
# 0xc0: write ok
# 0xce: write err
# 0xe0: erase ok
# 0xee: erase err
# 0xae: app crc err
# 0xa1: app mode err

check_file()

logging.debug("Starting Firmware Download (%s)" % args.file)

run_blmode()
sleep(0.5)

read_status()
sleep(0.5)

#erase
erase_aprom()
sleep(0.5)

read_status()
sleep(0.5)

#writing file...
binfile = open(args.file, "rb")

offset = 0
retry = 0
while True:
    datachunk = binfile.read(16)
    if not datachunk:
        break;
    hexlist = dumphex(datachunk)
    #print hexlist
    #print ipmi_writecmd(offset, hexlist)
    #print offset
    if (offset % 320 == 0):
        sys.stdout.write("\nWriting [0x%04x]" % offset)
        sys.stdout.flush()

    #print "Writing...[%04x]\r" % offset
    #print binascii.hexlify(datachunk)
    while True:
        ipmitool_write(offset, hexlist)
        #sleep(0.1)
	#while not ipmitool_verify():
	#    sleep(0.1)
        #sleep(0.1)
        #mod, state = read_status()
        #if state == 0xc0:
        #    break;
        #else:
        #    print "Retry............................................"
        #    retry = retry + 1
        chunk = read_chunk(offset)
        #print binascii.hexlify(chunk)

        if compare_chunk(chunk, datachunk):
            sys.stdout.write(".")
            sys.stdout.flush()
            break;
        else:
            #print "Retry..."
            sys.stdout.write("*")
            sys.stdout.flush()
            retry = retry + 1
            #logging.debug("Retry (offset %04x)" % offset)

    offset += 16
    #sleep(0.5)
    #ipmitool_read()

binfile.close
print("")
print("retry %d" % retry)
logging.debug("Total Retry: %d" % retry)
logging.debug("End...")

read_status()

run_appmode()
print("System will reboot now...")

sys.exit(0)

