#!/usr/bin/env python
import argparse
import sys
import traceback

# TODO: Change these descriptions and epilog, or leave blank.
PROGRAM_HANDLE = "{{project_slug}}"

DESCRIPTION = "Short application description."

EPILOG = """
Notes:
~~~~~~
  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
  incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
  nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
  Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore
  eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt
  in culpa qui officia deserunt mollit anim id est laborum.
"""


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
    return parser


def run(args: argparse.Namespace) -> int:
    """Entrypoint to the application.

    Import and run your code here.
    """
    # TODO: Implement call to library code
    print("Hello World!")
    return 0


def main() -> int:
    """`main` function

    Handles argument parsing with `argparse` hands it on to the `run`
    function that should call the library code as an application
    """

    args = arg_parser().parse_args()
    try:
        return run(args)
    except Exception:
        # Catch all exception that will ensure that the exception is printed and
        # that the error code is returned.
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
