#!/usr/bin/env python3

"""Traverse Makefile and print all help instructions"""
import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

TEXT_FMT_BOLD = "\033[1m"
TEXT_FMT_END = "\033[0m"
SEP = ";"


def expand_path(path: Path):
    """Expands variables from the given path and turns it into absolute path"""

    return os.path.abspath(os.path.expanduser(os.path.expandvars(path)))


def setup() -> argparse.Namespace:
    """Parse command-line arguments"""

    parser = argparse.ArgumentParser(
        description="Traverse Makefile and print all help instructions",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="If set, print verbose descriptions",
        required=False,
    )
    parser.add_argument(
        "--no-colorize",
        action="store_true",
        default=False,
        help="If set, colorizes the text-output",
        required=False,
    )
    args = parser.parse_args()

    return args


def gen_help(
    args: argparse.Namespace,
) -> Tuple[argparse.Namespace, Dict[str, List[str]]]:
    """Generate dict from help instructions in Makefile"""

    define_regex = re.compile("define (?P<target>.+)-help")
    end_ef_regex = re.compile("endef")
    help: Dict[str, List[str]] = {}
    key = ""
    description: List[str] = []
    with open(Path("Makefile")) as makefile:
        for line in makefile.readlines():
            if define_regex.match(line):
                match = define_regex.match(line)
                assert match
                key = match.group("target")
            elif end_ef_regex.match(line):
                help[key] = [
                    ln[1:].strip("\n") for ln in description if ln.startswith("#")
                ]
                key = ""
                description = []
            elif key:
                description.append(line)
    return (args, help)


def print_help(args: argparse.Namespace, help_text: Dict[str, List[str]]) -> None:
    """Print the help instructions"""

    print(
        "\n".join(
            [
                "Usage:",
                " ",
                f"  make help          {SEP} Brief target description",
                f"  make help-verbose  {SEP} Verbose target descriptions",
                f"  make [target]      {SEP} Invoke the given 'target'",
                " ",
                "Example:",
                " ",
                "  make install-all",
                " ",
                "Targets:",
                " ",
            ]
        )
    )
    width = max(len(k) for k in help_text)

    for key, description in sorted(help_text.items()):
        short = "".join(
            [key.ljust(width), f" {SEP}{description[0]}"]
            if args.no_colorize
            else [
                TEXT_FMT_BOLD,
                key.ljust(width),
                TEXT_FMT_END,
                f" {SEP}{description[0]}",
            ]
        )
        print(short)
        if args.verbose and len(description) > 1:
            for line in description[1:]:
                print(line)
            print("")


def main(args: argparse.Namespace) -> int:
    """Entry point"""

    try:
        print_help(*gen_help(args))
    except FileNotFoundError:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main(setup()))
