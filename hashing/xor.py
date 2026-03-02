#!/usr/bin/env python3
import argparse, base64

def xor(data, key):
    return bytes(a ^ key[i % len(key)] for i, a in enumerate(data))

def main():
    p = argparse.ArgumentParser()
    p.add_argument('action', choices=['encrypt', 'decrypt'])
    p.add_argument('data')
    p.add_argument('-k', '--key', required=True)
    args = p.parse_args()

    if args.action == 'encrypt':
        result = base64.b64encode(xor(args.data.encode(), args.key.encode())).decode()
        print(result)
    else:
        data = base64.b64decode(args.data)
        result = xor(data, args.key.encode()).decode('utf-8', errors='ignore')
        print(result)

if __name__ == '__main__':
    main()