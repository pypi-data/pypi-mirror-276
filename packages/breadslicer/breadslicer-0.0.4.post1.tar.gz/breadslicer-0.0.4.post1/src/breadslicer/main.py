#!/usr/bin/env python
import argparse
import pathlib
import sys
import traceback

from breadslicer.application.app import Application

# TODO: Change these descriptions and epilog, or leave blank.
PROGRAM_HANDLE = "breadslicer"

DESCRIPTION = (
    "Breadslicer is command line utility to create new python projects from templates."
)

EPILOG = """
Notes:
~~~~~~
*
"""

OUTPUT_HELP = (
    "Output directory, if this is not specified it will just use the"
    "project slug and place it in the directory in which the tool is run"
)


def arg_parser() -> argparse.ArgumentParser:
    """Function to implement argparse parameters

    NOTE: If this function gets out of hand, length wise, consider moving it to
    its own file(e.g. arg_parse.py)
    """
    parser = argparse.ArgumentParser(
        prog=PROGRAM_HANDLE,
        description=DESCRIPTION,
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-o", "--output", type=pathlib.Path, help=OUTPUT_HELP)
    return parser


def run(args: argparse.Namespace) -> int:
    """Entrypoint to the application."""
    application = Application("opinionated", args)
    application.run()

    return 0


def main() -> int:
    """`main` function

    Handles argument parsing with `argparse` hands it on to the `run`
    function that should call the library code as an application
    """

    args = arg_parser().parse_args()
    try:
        return run(args)
    except KeyboardInterrupt:
        print("Template generation was cancelled by user.")
        return 0
    except Exception:
        # Catch all exception that will ensure that the exception is printed and
        # that the error code is returned.
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
