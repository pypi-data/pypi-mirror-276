#!/usr/bin/env python3
# ==============================================================================
#
#          FILE:  dictionarymerger.py
#
#         USAGE:  ./scripts/dictionarymerger.py
#                 ./scripts/dictionarymerger.py --help
#
#   DESCRIPTION:  ---
#
#       OPTIONS:  ---
#
#  REQUIREMENTS:  - python3
#          BUGS:  ---
#         NOTES:  ---
#       AUTHORS:  Emerson Rocha <rocha[at]ieee.org>
# COLLABORATORS:  ---
#
#       COMPANY:  EticaAI
#       LICENSE:  GNU Affero General Public License v3.0 or later
#                 SPDX-License-Identifier: AGPL-3.0-or-later
#       VERSION:  v1.0.0
#       CREATED:  2023-05-06 22:24 BRT started, based on dictionarybuilder.py
#      REVISION:  --
# ==============================================================================

import argparse
import csv
# import re
import sys


__VERSION__ = "1.0.0"
PROGRAM = "dictionarymerger"
DESCRIPTION = """
------------------------------------------------------------------------------
For 2 or more output dictionaries from dictionarybuilder, merge them.

Simple strategy is *append* (e.g. similar to unix cat command, but sort again
the values and check inconsistencies).

[Next part NOT implemented yet]

The additional strategy is *transpose* value from dictionary A directly on
result of dictoryary B. Example:

    Input 1: X -> Y
    Input 2: Y -> Z
    Output:  X -> Z

------------------------------------------------------------------------------
""".format(
    PROGRAM, __VERSION__
)

__EPILOGUM__ = """
------------------------------------------------------------------------------
                            EXEMPLŌRUM GRATIĀ
------------------------------------------------------------------------------

    {0} --help

------------------------------------------------------------------------------
                            EXEMPLŌRUM GRATIĀ
------------------------------------------------------------------------------
""".format(
    PROGRAM
)

# Record separator
DICTIONARY_SEPARATOR = "␞"

STDIN = sys.stdin.buffer


class Cli:
    """Main CLI parser"""

    def __init__(self):
        """
        Constructs all the necessary attributes for the Cli object.
        """
        self.pyargs = None
        self.EXIT_OK = 0
        self.EXIT_ERROR = 1
        self.EXIT_SYNTAX = 2

    def make_args(self):
        """make_args"""
        parser = argparse.ArgumentParser(
            prog=PROGRAM,
            description=DESCRIPTION,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=__EPILOGUM__,
        )

        # @see https://stackoverflow.com/questions/5373474/multiple-positional-arguments-with-python-and-argparse
        # @TODO deal with both simple contatenation and transposition
        #       do not need to implement on this tool advanced input normalization
        parser.add_argument("input", help="path to CSV file on disk. Use - for stdin")

        parser.add_argument(
            "--input-append-file",
            help="The input delimiter",
            dest="in_append_files",
            default=None,
            action="append",
            required=False,
            nargs="?",
        )

        parser.add_argument(
            "--ignore-warnings",
            help="Ignore some errors (duplicated key / ambiguous results)",
            dest="ignore_warnings",
            action="store_true",
        )

        parser.add_argument(
            "--logfile",
            help="Path to a file to log warnings and other information",
            dest="logfile",
            nargs="?",
        )

        return parser.parse_args()

    def execute_cli(self, pyargs, stdin=STDIN, stdout=sys.stdout, stderr=sys.stderr):
        # with open(pyargs.input, "r", encoding=pyargs.in_encoding) if len(

        outdict = {}

        f_warnings = sys.stderr
        if pyargs.logfile:
            f_logfile = open(pyargs.logfile, "w", encoding="utf-8")
            f_warnings = f_logfile

        with open(pyargs.input, "r") if len(pyargs.input) > 1 else sys.stdin as csvfile:
            reader = csv.reader(csvfile, delimiter=DICTIONARY_SEPARATOR)

            for row in reader:
                # print(row)
                outdict[row[0]] = row[1]

            outdict_sorted = dict(sorted(outdict.items()))

            writer = csv.writer(
                sys.stdout, delimiter=DICTIONARY_SEPARATOR, quoting=csv.QUOTE_MINIMAL
            )

        if pyargs.in_append_files:
            for dfile in pyargs.in_append_files:
                # @TODO deal with duplicates
                with open(dfile, "r") as csvfile:
                    reader = csv.reader(csvfile, delimiter=DICTIONARY_SEPARATOR)
                    for row in reader:
                        # print(dfile)
                        # print(row)
                        _k = row[0]
                        _v = row[1]
                        if (
                            _k in outdict
                            and outdict[_k] != _v
                            and not pyargs.ignore_warnings
                        ):
                            print(f"{_k} repeated", file=f_warnings)
                        outdict[_k] = _v

        for key, value in outdict_sorted.items():
            writer.writerow([key, value])

        if pyargs.logfile:
            f_logfile.close()

        return self.EXIT_OK


def _file_to_dict(file: str) -> dict:
    pass


def exec_from_console_scripts():
    main = Cli()
    args = main.make_args()
    main.execute_cli(args)


if __name__ == "__main__":
    cli_2600 = Cli()
    args = cli_2600.make_args()
    # pyargs.print_help()

    # args.execute_cli(args)
    cli_2600.execute_cli(args)
