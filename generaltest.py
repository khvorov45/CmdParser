"""General-use cmdparser test"""

import sys

from colorama import init, Fore

from cmdparserkhv import CmdParser, Cmdent

init(autoreset=True)

def run_parser(args):
    """Runs the parser with some sample options"""
    opts = {
        "-o1": Cmdent("option1", allowed=["a", "b"]),
        "-o2": Cmdent("option2")
    }
    opts_parsed = CmdParser(args, opts)
    print(opts_parsed.get_opts())

def get_o1(arg=None):
    """Gets argument 1"""
    default = ["a"]
    if arg is None:
        return default
    allowed = ["a", "b"]
    if arg not in allowed:
        print_yellow("option " + arg + " not recognised, using default")
        return default
    return arg

def print_yellow(string):
    """Prints string in yellow"""
    print(Fore.YELLOW + string)

if __name__ == "__main__":
    run_parser(sys.argv)
