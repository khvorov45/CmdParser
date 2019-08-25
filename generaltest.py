"""General-use cmdparser test"""

import sys

from colorama import init, Fore

from cmdparserkhv import CmdParser

init(autoreset=True)

def run_parser(args):
    """Runs the parser with some sample options"""
    opts = {
        "-o1": ["option1", get_o1],
        "-o2": ["option2", False]
    }
    opts_parsed = CmdParser(args, opts)
    print(opts_parsed)

def get_o1(arg):
    """Gets argument 1"""
    allowed = ["a", "b"]
    default = ["a"]
    if arg not in allowed:
        print_yellow("option " + arg + " not recognised, using default")
        return default
    return arg

def print_yellow(string):
    """Prints string in yellow"""
    print(Fore.YELLOW + string)

if __name__ == "__main__":
    run_parser(sys.argv)
