#!/usr/bin/env python3
import argparse, base64, sys

def main():
    p = argparse.ArgumentParser()
    p.add_argument('data')
    p.add_argument('-k', '--key', required=True)
    p.add_argument('-i', '--iv', required=True)
    args = p.parse_args()

    data = base64.b64decode(args.data)
    key = args.key.encode()
    iv = args.iv.encode()

    # Try simple XOR with the key
    result = bytearray()
    for i, byte in enumerate(data):
        result.append(byte ^ key[i % len(key)])

    print("XOR result:", result.decode('utf-8', errors='ignore'))

    # Try XOR with IV
    result2 = bytearray()
    for i, byte in enumerate(data):
        result2.append(byte ^ iv[i % len(iv)])

    print("XOR with IV:", result2.decode('utf-8', errors='ignore'))

if __name__ == '__main__':
    main()