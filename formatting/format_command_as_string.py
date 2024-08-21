import argparse
import ast

parser = argparse.ArgumentParser()
parser.add_argument('command', type=str, help='The input string argument')

args = parser.parse_args()

command_list = ast.literal_eval(args.command)

print(" ".join(command_list))