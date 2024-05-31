#!/usr/bin/env python3
# ==============================================================================
#
#          FILE:  json2csv.py
#
#         USAGE:  ./scripts/json2csv.py
#                 ./scripts/json2csv.py --help
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
#       CREATED:  2023-05-06 19:32 BRT
#      REVISION:  --
# ==============================================================================

import argparse
import csv
import json
import sys
from typing import Dict


__VERSION__ = "1.0.0"
PROGRAM = "json2csv"
DESCRIPTION = """
------------------------------------------------------------------------------
Convert JSON input file into CSV output file. If have nested values,
the output will contatenate the names with "."

------------------------------------------------------------------------------
""".format(
    PROGRAM, __VERSION__
)

__EPILOGUM__ = """
------------------------------------------------------------------------------
                            EXEMPLŌRUM GRATIĀ
------------------------------------------------------------------------------

    {0} --help

    {0} input.json > output.csv

------------------------------------------------------------------------------
                            EXEMPLŌRUM GRATIĀ
------------------------------------------------------------------------------
""".format(
    PROGRAM
)

# Record separator
# DICTIONARY_SEPARATOR = "␞"

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

        parser.add_argument("input", help="path to JSON file on disk. Use - for stdin")

        parser.add_argument(
            "--input-data-base",
            help="In case input data already is not a array of objects/list, "
            "this allow explicitly inform the base. Often is 'data'.",
            dest="in_base",
            default=None,  # Defaults to auto
            required=False,
            nargs="?",
        )

        parser.add_argument(
            "--output-delimiter",
            help="The input delimiter",
            dest="out_delimiter",
            default=",",
            required=False,
            nargs="?",
        )

        return parser.parse_args()

    def execute_cli(self, pyargs, stdin=STDIN, stdout=sys.stdout, stderr=sys.stderr):
        _checkfor = ["data"]
        data = False

        if pyargs.in_base:
            _checkfor.insert(0, pyargs.in_base)

        with open(pyargs.input, "r") if len(
            pyargs.input
        ) > 1 else sys.stdin as jsonfile:
            # parsed = json.loads(jsonfile)
            parsed = json.load(jsonfile)

            if isinstance(parsed, list):
                data = parsed
            elif isinstance(parsed, dict):
                for item in _checkfor:
                    if item in parsed:
                        data = parsed[item]
                        break

                if data is False:
                    raise SyntaxError(["Key not found. Options ", parsed.keys()])

            result_data = []

            fieldnames = []

            for item in data:
                _result = in_obiectum_planum(item)
                for _k in _result.keys():
                    if _k not in fieldnames:
                        fieldnames.append(_k)
                result_data.append(_result)

            writer = csv.DictWriter(
                sys.stdout, fieldnames=fieldnames, delimiter=pyargs.out_delimiter
            )

            writer.writeheader()

            for item in result_data:
                writer.writerow(item)

            return self.EXIT_OK


def in_obiectum_planum(rem: Dict, pydictsep: str = ".", pylistsep: str = " ") -> dict:
    """in_obiectum_planum Flatten a nested python object

    Trivia:
      - obiectum, https://en.wiktionary.org/wiki/obiectum#Latin
      - recursiōnem, https://en.wiktionary.org/wiki/recursio#Latin
      - praefīxum, https://en.wiktionary.org/wiki/praefixus#Latin
      - plānum, https://en.wiktionary.org/wiki/planus

    Args:
        rem (dict): The object to flatten
        pydictsep (pydictsep, optional): The separator for python dict keys
        pylistsep (pydictsep, optional): The separator for python list values

    Returns:
        [dict]: A flattened python dictionary

    Exemplōrum gratiā (et Python doctest, id est, testum automata):

    >>> testum1 = {'a0': {'a1': {'a2': 'va'}}, 'b0': [1, 2, 3]}
    >>> in_obiectum_planum(testum1)
    {'a0.a1.a2': 'va', 'b0': '1 2 3'}

    >>> in_obiectum_planum(testum1)
    {'a0.a1.a2': 'va', 'b0': '1 2 3'}

    >>> in_obiectum_planum(testum1, pylistsep=',')
    {'a0.a1.a2': 'va', 'b0': '1,2,3'}

    >>> in_obiectum_planum(testum1, pydictsep='->')
    {'a0->a1->a2': 'va', 'b0': '1 2 3'}

    # This is not designed to flat arrays, str, None, int, ..., only dict
    >>> in_obiectum_planum([1, 2, 3, 4])
    Traceback (most recent call last):
    ...
    TypeError: in_obiectum_planum non dict<class 'list'>
    """
    resultatum = {}

    if not isinstance(rem, dict):
        raise TypeError("in_obiectum_planum non dict" + str(type(rem)))

    def recursionem(rrem, praefixum: str = ""):
        praefixum_ad_hoc = "" if praefixum == "" else praefixum + pydictsep
        if isinstance(rrem, dict):
            for clavem in rrem:
                recursionem(rrem[clavem], praefixum_ad_hoc + clavem)
        elif isinstance(rrem, list):
            resultatum[praefixum] = pylistsep.join(map(str, rrem))
        else:
            resultatum[praefixum] = rrem

    recursionem(rem)

    return resultatum


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
