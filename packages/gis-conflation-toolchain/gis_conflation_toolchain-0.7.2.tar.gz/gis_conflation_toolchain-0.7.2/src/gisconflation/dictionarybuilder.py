#!/usr/bin/env python3
# ==============================================================================
#
#          FILE:  dictionarybuilder.py
#
#         USAGE:  ./scripts/dictionarybuilder.py
#                 ./scripts/dictionarybuilder.py --help
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
import re
import sys


__VERSION__ = "1.0.0"
PROGRAM = "dictionarybuilder"
DESCRIPTION = """
------------------------------------------------------------------------------
Convert 2 or more columns of one CSV input file into a dictionary (a sorted
2 column RS delimited file) optimized to be used by other tools as simple
pivot file to replace or append new values to existing datasets

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

        parser.add_argument("input", help="path to CSV file on disk. Use - for stdin")

        parser.add_argument(
            "--input-delimiter",
            help="The input delimiter",
            dest="in_delimiter",
            default=",",
            required=False,
            nargs="?",
        )

        parser.add_argument(
            "--input-encoding",
            help="The input encoding",
            dest="in_encoding",
            default="utf-8",
            required=False,
            nargs="?",
        )

        parser.add_argument(
            "--input-fieldnames",
            help="If the input CSV does not have a header, specify here. "
            "Use | as separator (if a field de de facto have |, then use \|). "
            "Example: --input-fieldnames='field with \| on it|another field'",
            dest="in_fieldnames",
            # default="utf-8",
            required=False,
            nargs="?",
        )

        parser.add_argument(
            "--dict-target-key",
            help="Field name to represent the primary key to convert data "
            "Defaults to first column. Example: "
            "--dict-target-key='id'",
            dest="dict_target",
            required=False,
            nargs="?",
        )

        parser.add_argument(
            "--dict-source-key",
            help="Field name to be used as source to convert data to target key. "
            "If undefined, defaults to all fields which are not the "
            "--dict-target-key. Example: "
            "--dict-source-key='name' --dict-source-key='title' ",
            dest="dict_sources",
            action="append",
            required=False,
            nargs="?",
        )

        parser.add_argument(
            "--transform-uppercase",
            help="Force all source values to UPPERCASE",
            dest="t_uppercase",
            action="store_true",
        )

        parser.add_argument(
            "--transform-lowercase",
            help="Force all source values to lowercase",
            dest="t_lowercase",
            action="store_true",
        )

        parser.add_argument(
            "--transform-no-latin-accents",
            help="Remove some diacrilics of latin script",
            dest="t_nolatinaccents",
            action="store_true",
        )

        parser.add_argument(
            "--logfile",
            help="Path to a file to log warnings and other information",
            dest="logfile",
            nargs="?",
        )

        parser.add_argument(
            "--ignore-warnings",
            help="Ignore some errors (duplicated key / ambiguous results)",
            dest="ignore_warnings",
            action="store_true",
        )

        return parser.parse_args()

    def execute_cli(self, pyargs, stdin=STDIN, stdout=sys.stdout, stderr=sys.stderr):
        # @TODO implement strict run (fail if repeated source falues)
        # @TODO implement UPPER, lower and remove-accents options

        f_warnings = sys.stderr
        if pyargs.logfile:
            f_logfile = open(pyargs.logfile, "w", encoding="utf-8")
            f_warnings = f_logfile

        # @TODO stdin does not yet allow non UTF8 customization (will pass as it is)
        # @see https://stackoverflow.com/questions/5004687
        with open(pyargs.input, "r", encoding=pyargs.in_encoding) if len(
            pyargs.input
        ) > 1 else sys.stdin as csvfile:
            if pyargs.in_fieldnames:
                _in_fieldnames = re.split(r"(?<!\\)\|", pyargs.in_fieldnames)
                # _in_fieldnames = re.split(r"", pyargs.in_fieldnames)

                reader = csv.DictReader(
                    csvfile, fieldnames=_in_fieldnames, delimiter=pyargs.in_delimiter
                )
            else:
                reader = csv.DictReader(csvfile, delimiter=pyargs.in_delimiter)

            # reader = csv.DictReader(csvfile, delimiter=pyargs.in_delimiter)

            firstline = next(reader)
            # print(firstline)

            _fieldnames = firstline.keys()
            # print(_fieldnames)

            if pyargs.dict_target:
                dict_target = pyargs.dict_target
            else:
                # dict_target = _fieldnames[0]
                dict_target = list(_fieldnames).pop(0)

            if pyargs.dict_sources:
                dict_sources = pyargs.dict_sources
            else:
                _temp = list(_fieldnames)
                _temp.remove(dict_target)
                dict_sources = _temp

            writer = csv.writer(
                sys.stdout, delimiter=DICTIONARY_SEPARATOR, quoting=csv.QUOTE_MINIMAL
            )

            outdict = {}
            # @TODO This part is a bit duplicated. Could be better.
            # #     Remove duplicated code
            for item in dict_sources:
                if not firstline[item] or len(firstline[item]) == 0:
                    continue

                _v = firstline[item].strip()
                _k = firstline[dict_target].strip()

                if pyargs.t_nolatinaccents:
                    _v = _v.lower()
                    # Obviously incomplete
                    _v = re.sub(r"[àáâãäå]", "a", _v)
                    _v = re.sub(r"[èéêë]", "e", _v)
                    _v = re.sub(r"[ìíîï]", "i", _v)
                    _v = re.sub(r"[òóôõö]", "o", _v)
                    _v = re.sub(r"[ñ]", "n", _v)
                    _v = re.sub(r"[ç]", "c", _v)

                if pyargs.t_lowercase:
                    _v = _v.lower()
                elif pyargs.t_uppercase:
                    _v = _v.upper()

                if _k in outdict and outdict[_k] != _v and not pyargs.ignore_warnings:
                    print(f"{_k} repeated", file=f_warnings)
                    continue

                outdict[_k] = _v

            for row in reader:
                for item in dict_sources:
                    if not row[item] or len(row[item]) == 0:
                        continue

                    _v = row[item].strip()
                    _k = row[dict_target].strip()

                    if pyargs.t_nolatinaccents:
                        _v = _v.lower()
                        # Obviously incomplete
                        _v = re.sub(r"[àáâãäå]", "a", _v)
                        _v = re.sub(r"[èéêë]", "e", _v)
                        _v = re.sub(r"[ìíîï]", "i", _v)
                        _v = re.sub(r"[òóôõö]", "o", _v)
                        _v = re.sub(r"[ñ]", "n", _v)
                        _v = re.sub(r"[ç]", "c", _v)

                    if pyargs.t_lowercase:
                        _v = _v.lower()
                    elif pyargs.t_uppercase:
                        _v = _v.upper()

                    if (
                        _k in outdict
                        and outdict[_k] != _v
                        and not pyargs.ignore_warnings
                    ):
                        print(f"{_k} repeated", file=f_warnings)
                        continue

                    outdict[_k] = _v

                    # outdict[firstline[item].strip()] = firstline[dict_target].strip()
                # writer.writerow(row)

            outdict_sorted = dict(sorted(outdict.items()))

            # print(outdict)
            # outdict

            for key, value in outdict_sorted.items():
                writer.writerow([key, value])

            # # writer.writeheader()
            # writer.writerow(firstline)

            # for row in reader:
            #     writer.writerow(row)

        if pyargs.logfile:
            f_logfile.close()

        return self.EXIT_OK


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
