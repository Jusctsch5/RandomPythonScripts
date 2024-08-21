#!/usr/bin/env python3

import argparse
import requests
import os
import subprocess
import json

symbol_base_url = "https://repository.mdh.quantum.com:8443/repository/symbols"
minidump_base_url = base_url = "https://repository.mdh.quantum.com:8443/repository/minidumps"
stackwalk="./bins/minidump_stackwalk"


def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)
        return True

    return False


def convert_string(s):
    s = s.upper()  # Convert the string to all uppercase
    prefix = s[:2]  # Extract the first two characters as the prefix
    s_parts = [s[i:i+2] for i in range(0, len(s), 2)][1:]  # Split the remaining string into pairs of characters
    s_with_slashes = '/'.join(s_parts)  # Join the pairs of characters with slashes
    path = prefix + '/' + s_with_slashes + '/' + s
    return path


def executable(content):
    modules = content['modules']
    main = content['main_module']
    main_mod = modules[main]
    exec = main_mod['filename']

    return exec


def cache_symbols(symdir, filename, sym_id):
    sym_file = os.path.join(symdir, filename, sym_id, filename + ".sym")
    if os.path.exists(sym_file):
        return

    # These are not happening
    if 'cpython' in filename:
        return

    sym_url = symbol_base_url + '/' + convert_string(sym_id)

    response = requests.get(sym_url)
    if response.status_code == 200:
        print('+', end='', flush=True)
        header = response.text.splitlines()[0]

        columns = header.split(" ")
        name = columns[4]

        mkdir(symdir + "/" + name)
        mkdir(symdir + "/" + name + "/" + sym_id)
        sym_file = symdir + "/" + name + "/" + sym_id + "/" + name + ".sym"

        with open(sym_file, "wb") as handle:
            handle.write(response.text.encode("utf-8"))
    else:
        print('-', end='', flush=True)


def summarize_json_dump(dump):
    with open(dump, 'r') as file:
        content = json.load(file)

    exec = executable(content)

    crash_thread = content['crashing_thread']
    frames = crash_thread['frames']

    function = frames[0]['function']
    line = frames[0]['line']
    missing = frames[0]['missing_symbols']

    if missing and not frames[1]['missing_symbols']:
        missing = False
        function = frames[1]['function']
        line = frames[1]['line']

    if function == "__ot_panic":
        function = frames[1]['function']
        line = frames[1]['line']
        reason = 'Panic'
    else:
        reason = 'Crash'

    if function:
        summary = f'{ exec } { reason } at { function }:{ line }'
    else:
        if missing:
            summary = 'No symbols'
        else:
            summary = f'Examine dump { dump }'

    return summary


def process_dump(workdir,
                 symdir,
                 minidump_uuid,
                 brief = False,
                 keep = False,
                 silent = False):

    mkdir(workdir)
    mkdir(symdir)

    minidump_url = minidump_base_url + "/" + minidump_uuid

    minidump_file = os.path.join(workdir, 'dumps', minidump_uuid + ".dmp")

    mkdir(os.path.join(workdir, 'dumps'))

    if not os.path.exists(minidump_file):
        print("Fetching " + minidump_url)
        response = requests.get(minidump_url, stream=True)

        with open(minidump_file, "wb") as handle:
            for data in response.iter_content():
                handle.write(data)

        if response.status_code != 200:
            print("Failed to obtain minidump, check if provided crash ID is valid")
            return None

    cmd = [stackwalk, minidump_file, symdir]
    result = subprocess.run(cmd, capture_output=True)
    print("running command as \n", " ".join(cmd))
    output = result.stdout.decode("utf-8")
    try:
        content = json.loads(output)
    except json.JSONDecodeError:
        print("Failed to decode minidump with output " + output)
        return None

    modules = content['modules']
    exec = executable(content)

    print('Symbols: ', end='', flush=True)
    for module in modules:
        loaded = module['loaded_symbols']

        if not loaded:
            filename = module['filename']
            sym_id = module['debug_id']

            cache_symbols(symdir, filename, sym_id)
    print('')

    mkdir(os.path.join(workdir, exec))
    mkdir(os.path.join(workdir, exec, 'json'))
    cyborg = os.path.join(workdir, exec, 'json', minidump_uuid + ".json")

    cmd = [stackwalk]
    if brief:
        cmd += ['--brief']
    cmd += ['--cyborg', cyborg]
    cmd += [minidump_file, '--symbols-path', symdir]
    result = subprocess.run(cmd, capture_output=True)

    content = result.stdout.decode("utf-8")

    mkdir(os.path.join(workdir, exec, 'text'))

    text_out = os.path.join(workdir, exec, 'text', minidump_uuid + ".txt")
    with open(text_out, "w") as file:
        file.write(content)

    summarize_json_dump(cyborg)

    if not silent:
        print(content)

    if keep:
        mkdir(os.path.join(workdir, exec, 'minidumps'))
        os.rename(minidump_file,
                  os.path.join(workdir, exec, 'minidumps', minidump_uuid + ".dmp"))
    else:
        os.unlink(minidump_file)

    return summarize_json_dump(cyborg)


if __name__ == "__main__":

    parser = argparse.ArgumentParser('Post process minidumps')
    parser.add_argument('-o', '--output', metavar='dir', default='/tmp/minidumps', help='Directory for output')
    parser.add_argument('-S', '--symbols', default="", help='Directory for symbol cache')
    parser.add_argument('uuid', help="Minidump uuid")
    parser.add_argument('--url', help='Base URL for minidumps')

    args = parser.parse_args()

    outdir = args.output
    if args.symbols:
        symdir = args.symbols
    else:
        symdir = os.path.expanduser('~/.myriad_symbols')

    mkdir(symdir)

    res = process_dump(outdir, symdir, args.uuid)


    # https://repository.mdh.quantum.com/repository/minidumps/e38bce4d-f4fd-40bb-bf48-7abe0c3981b4
    # https://repository.mdh.quantum.com/repository/minidumps/e38bce4d-f4fd-40bb-bf48-7abe0c3981b4
