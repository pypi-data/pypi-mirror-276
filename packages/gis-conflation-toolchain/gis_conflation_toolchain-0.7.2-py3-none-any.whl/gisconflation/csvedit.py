#!/usr/bin/env python3
# ==============================================================================
#
#          FILE:  csvedit.py
#
#         USAGE:  ./scripts/csvedit.py
#                 ./scripts/csvedit.py --help
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
#       VERSION:  v0.5.0
#       CREATED:  2023-05-06 16:54 BRT started, based on csv2geojson.py
#      REVISION:  --
# ==============================================================================


# import geopandas
# import os
import argparse
import csv

# import json
import re
import sys

from gisconflation.util import parse_argument_values

# import string

# from gisconflation.util import parse_argument_values

# try:
#     import geocoder
# except ImportError:
#     raise ImportError("Dependency not found. Please: pip install geocoder")
#
# # https://geocoder.readthedocs.io/providers/OpenStreetMap.html
# print(geocoder.osm('Mountain View, CA'))

# geocode 'New York city' --provider osm --out geojson | jq .

__VERSION__ = "0.5.0"
PROGRAM = "csvedit"
DESCRIPTION = """
------------------------------------------------------------------------------
CSV simple command line editor

------------------------------------------------------------------------------
""".format(
    PROGRAM, __VERSION__
)

# https://www.rfc-editor.org/rfc/rfc7946
# The GeoJSON Format
# https://www.rfc-editor.org/rfc/rfc8142
# GeoJSON Text Sequences

# __EPILOGUM__ = ""
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

        # parser.add_argument(
        #     "--lat",
        #     help="the name of the latitude column",
        #     dest="lat",
        #     required=True,
        #     nargs="?",
        # )

        # parser.add_argument(
        #     "--lon",
        #     help="the name of the longitude column",
        #     dest="lon",
        #     required=True,
        #     nargs="?",
        # )

        # parser.add_argument(
        #     "--filter-contain",
        #     help="Filter one or more fields for contain a string"
        #     "Use '|||' to divide the field and the string. "
        #     "Accept multiple values. "
        #     "Example: "
        #     "--filter-contain='name|||hospital'",
        #     dest="filter_contain",
        #     nargs="?",
        #     action="append",
        # )

        # parser.add_argument(
        #     "--contain-or",
        #     help="If defined, only results that match at least one clause"
        #     " will appear on output. Accept multiple values."
        #     "--contain-or=tag1=value1 --contain-or=tag2=value2",
        #     dest="contain_or",
        #     nargs="?",
        #     action="append",
        # )

        # parser.add_argument(
        #     "--contain-and",
        #     help="If defined, only results that match all clauses"
        #     " will appear on output. Accept multiple values."
        #     "--contain-and=tag1=value1 --contain-and=tag2=value2",
        #     dest="contain_and",
        #     nargs="?",
        #     action="append",
        # )

        # parser.add_argument(
        #     "--contain-and-in",
        #     help="Alternative to -contain-and where values for a "
        #     "single field are a list. Separe values with ||"
        #     "Accept multiple values."
        #     "--contain-and=tag_a=valuea1||valuea2||valuea3",
        #     dest="contain_and_in",
        #     nargs="?",
        #     action="append",
        # )

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
            "--output-delimiter",
            help="The output delimiter",
            dest="out_delimiter",
            default=",",
            required=False,
            nargs="?",
        )

        filter_group = parser.add_argument_group("Filter rows")

        filter_group.add_argument(
            "--contain-and",
            help="If defined, only results that match all clauses"
            " will appear on output. Accept multiple values."
            "--contain-and=tag1=value1 --contain-and=tag2=value2",
            dest="contain_and",
            nargs="?",
            action="append",
        )

        filter_group.add_argument(
            "--contain-and-regex",
            help="If defined, only results that match all clauses"
            " will appear on output. Accept multiple values."
            "Syntax is python regex. https://docs.python.org/3/library/re.html"
            "Example: "
            "--contain-and-regex='name|||hospital.+'",
            dest="contain_and_regex",
            nargs="?",
            action="append",
        )

        filter_group.add_argument(
            "--filter-contain",
            help="Filter one or more fields for contain a string"
            "Use '|||' to divide the field and the string. "
            "Accept multiple values. "
            "Example: "
            "--filter-contain='name|||hospital'",
            dest="filter_contain",
            nargs="?",
            action="append",
        )

        # parser.add_argument(
        #     "--output-type",
        #     help="Change the default output type",
        #     dest="outfmt",
        #     default="GeoJSON",
        #     # geojsom
        #     # geojsonl
        #     choices=[
        #         "GeoJSON",
        #         "GeoJSONSeq",
        #     ],
        #     required=False,
        #     nargs="?",
        # )

        # parser.add_argument(
        #     "--ignore-warnings",
        #     help="Ignore some errors (such as empty latitude/longitude values)",
        #     dest="ignore_warnings",
        #     action="store_true",
        # )

        # cast_group = parser.add_argument_group(
        #     "Convert/preprocess data from input, including generate new fields"
        # )

        # cast_group.add_argument(
        #     "--cast-integer",
        #     help="Name of input fields to cast to integer. "
        #     "Use | for multiple. "
        #     "Example: <[ --cast-integer='field_a|field_b|field_c' ]>",
        #     dest="cast_integer",
        #     nargs="?",
        #     type=lambda x: x.split("|"),
        #     default=None,
        # )

        # cast_group.add_argument(
        #     "--cast-float",
        #     help="Name of input fields to cast to float. "
        #     "Use | for multiple. "
        #     "Example: <[ --cast-float='latitude|longitude|field_c' ]>",
        #     dest="cast_float",
        #     nargs="?",
        #     type=lambda x: x.split("|"),
        #     default=None,
        # )

        # cast_group.add_argument(
        #     "--column-copy-to",
        #     help="Add extra comluns. "
        #     "For multiple, use multiple times this parameter. "
        #     "Source vs destiny column must be divided by |. "
        #     "Example: <[ --column-copy-to='ORIGINAL_FIELD_PT|name:pt' "
        #     "--column-copy-to='CNPJ|ref:vatin' ]>",
        #     dest="column_copy",
        #     nargs="?",
        #     # type=lambda x: x.split("||"),
        #     action="append",
        #     default=None,
        # )

        # cast_group.add_argument(
        #     "--value-fixed",
        #     help="Define a fixed string for every value of a column, "
        #     "For multiple, use multiple times this parameter. "
        #     "Source vs destiny column must be divided by |. "
        #     "Example: <[ --value-fixed='source|BR:DATASUS' ]>",
        #     dest="value_fixed",
        #     nargs="?",
        #     # type=lambda x: x.split("||"),
        #     action="append",
        #     default=None,
        # )

        # cast_group.add_argument(
        #     "--value-prepend",
        #     help="Prepend a custom string to all values in a column. "
        #     "For multiple, use multiple times this parameter. "
        #     "Source vs destiny column must be divided by |. "
        #     "Example: <[ --value-prepend='ref:vatin|BR' ]>",
        #     dest="value_prepend",
        #     nargs="?",
        #     # type=lambda x: x.split("||"),
        #     action="append",
        #     default=None,
        # )

        # cast_group.add_argument(
        #     "--value-postcode-br",
        #     help="One or more column names to format as if was Brazilan postcodes, CEP",
        #     dest="value_postcode_br",
        #     nargs="?",
        #     type=lambda x: x.split("|"),
        #     default=None,
        # )

        # cast_group.add_argument(
        #     "--value-phone-br",
        #     help="One or more column names to format as Brazilian "
        #     "phone/fax/WhatsApp number",
        #     dest="value_phone_br",
        #     nargs="?",
        #     type=lambda x: x.split("|"),
        #     default=None,
        # )

        # cast_group.add_argument(
        #     "--value-name-place-br",
        #     help="One or more columsn to format as name of place (Locale BR)",
        #     dest="value_name_place_br",
        #     nargs="?",
        #     type=lambda x: x.split("|"),
        #     default=None,
        # )

        # cast_group.add_argument(
        #     "--value-name-street-br",
        #     help="One or more columsn to format as name of street "
        #     "(Locale BR, 'logradouro') ",
        #     dest="value_name_street_br",
        #     nargs="?",
        #     type=lambda x: x.split("|"),
        #     default=None,
        # )

        return parser.parse_args()

    def execute_cli(self, pyargs, stdin=STDIN, stdout=sys.stdout, stderr=sys.stderr):
        # input_file = STDIN if pyargs.input == "-" else pyargs.input

        # print("TODO")

        _contain_and = {}
        if pyargs.contain_and:
            for item in pyargs.contain_and:
                if item:
                    if item.find("="):
                        _key, _val = item.split("=")
                        _contain_and[_key] = _val
                    else:
                        _contain_and[_key] = True

        filter_contain = parse_argument_values(pyargs.filter_contain)
        contain_and_regex = parse_argument_values(pyargs.contain_and_regex)

        # @TODO stdin does not yet allow non UTF8 customization (will pass as it is)
        # @see https://stackoverflow.com/questions/5004687
        with open(pyargs.input, "r", encoding=pyargs.in_encoding) if len(
            pyargs.input
        ) > 1 else sys.stdin as csvfile:
            if pyargs.in_fieldnames:
                _in_fieldnames = re.split(r"(?<!\\)\|", pyargs.in_fieldnames)
                # _in_fieldnames = re.split(r"", pyargs.in_fieldnames)
                # print(_in_fieldnames)

                reader = csv.DictReader(
                    csvfile, fieldnames=_in_fieldnames, delimiter=pyargs.in_delimiter
                )
            else:
                reader = csv.DictReader(csvfile, delimiter=pyargs.in_delimiter)

            # reader = csv.DictReader(csvfile, delimiter=pyargs.in_delimiter)

            firstline = next(reader)

            _fieldnames = firstline.keys()
            writer = csv.DictWriter(
                sys.stdout, fieldnames=_fieldnames, delimiter=pyargs.out_delimiter
            )

            writer.writeheader()
            # writer.writerow(firstline)

            reader2 = list(reader)
            reader2.insert(0, firstline)

            # @TODO bug with both conditions must be fixed.

            # for row in reader:
            for row in reader2:
                # @TODO move out of here
                if _contain_and:
                    _count = len(_contain_and.keys())

                    for _key, _val in _contain_and.items():
                        if _key not in row:
                            raise SyntaxError(f"key {_key} not in {row}")
                            # return False
                        # print(item)
                        if _val is not True and _val != row[_key]:
                            continue
                        _count -= 1

                    if _count > 0:
                        continue

                if filter_contain:
                    # raise ValueError(filter_contain)
                    _count2 = len(filter_contain.keys())

                    for _key, _val in filter_contain.items():
                        if not isinstance(_val, bool):
                            _val = _val.lower()

                        if _key not in row:
                            raise SyntaxError(f"key {_key} not in {row}")
                            # return False

                        if _val is not True and row[_key].lower().find(_val) == -1:
                            continue
                        _count2 -= 1

                    if _count2 > 0:
                        continue

                if contain_and_regex:
                    # raise ValueError(filter_contain)
                    _count3 = len(contain_and_regex.keys())

                    for _key, _regex in contain_and_regex.items():
                        # _val = _val.lower()

                        if _key not in row:
                            raise SyntaxError(f"key {_key} not in {row}")
                            # return False
                        _result = re.match(_regex, row[_key])

                        # if _val is not True and row[_key].lower().find(_val) == -1:
                        if not _result:
                            continue
                        _count3 -= 1

                    if _count3 > 0:
                        continue

                writer.writerow(row)

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
