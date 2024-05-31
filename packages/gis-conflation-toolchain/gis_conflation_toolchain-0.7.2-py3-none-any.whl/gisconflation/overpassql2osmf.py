#!/usr/bin/env python3
# ==============================================================================
#
#          FILE:  overpassql2osmf.py
#
#         USAGE:  overpassql2osmf --help
#
#   DESCRIPTION:  ---
#
#       OPTIONS:  ---
#
#  REQUIREMENTS:  - python3
#                   - pip install pandas (https://pandas.pydata.org/)
#          BUGS:  ---
#         NOTES:  ---
#       AUTHORS:  Emerson Rocha <rocha[at]ieee.org>
# COLLABORATORS:  ---
#
#       COMPANY:  EticaAI
#       LICENSE:  GNU Affero General Public License v3.0 or later
#                 SPDX-License-Identifier: AGPL-3.0-or-later
#       VERSION:  v0.2.0
#       CREATED:  2023-04-26 01:04 BRT
#      REVISION:  ---
# ==============================================================================

# ./src/gisconflation/overpassql2osmf.py --help
# ./src/gisconflation/overpassql2osmf.py tests/data/cnes.overpassql > tests/temp/cnes.osm.json
# overpassql2osmf tests/data/cnes.overpassql > tests/temp/cnes.osm.json
# overpassql2osmf tests/data/cnes.overpassql | osmf2geojson > tests/temp/cnes.osm.geojson
# ./src/gisconflation/overpassql2osmf.py '[out:csv(::id,::type,"name")]; area[name="Bonn"]; nwr(area)[railway=station]; out;' > tests/temp/bonn.osm.csv


# overpassql2osmf tests/data/cnes.overpassql > tests/temp/cnes.osm
# osmium sort tests/temp/cnes.osm --output-format osm > tests/temp/cnes-sorted.osm
# osmium export tests/temp/cnes-sorted.osm --output-format geojson > tests/temp/cnes.osm.geojson

# osmf2geojson tests/temp/cnes-sorted.osm > tests/temp/cnes.osm.geojson

import os
import sys
import argparse

import requests

# import pandas as pd

__VERSION__ = "0.2.0"
PROGRAM = "overpassql2osmf"
DESCRIPTION = """
------------------------------------------------------------------------------
{0} v{1} convert Overpass Query Language to am OSM File (XML)

------------------------------------------------------------------------------
""".format(
    PROGRAM, __VERSION__
)

__EPILOGUM__ = """
------------------------------------------------------------------------------
                            EXEMPLŌRUM GRATIĀ
------------------------------------------------------------------------------
Input file contains Overpass query . . . . . . . . . . . . . . . . . . . . . .
    {0} tests/data/cnes.overpassql > tests/temp/cnes.osm

CSV Output (requires special Overpass query) . . . . . . . . . . . . . . . . .

    {0} '[out:csv(::id,::type,"name")]; area[name="Bonn"]; nwr(area)[railway=station]; out;' \
> tests/temp/bonn.osm.csv
------------------------------------------------------------------------------
                            EXEMPLŌRUM GRATIĀ
------------------------------------------------------------------------------
""".format(
    PROGRAM
)

STDIN = sys.stdin.buffer
OVERPASS_INTERPRETER = os.getenv(
    "OVERPASS_INTERPRETER", "https://overpass-api.de/api/interpreter"
)


class Cli:
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

        parser.add_argument(
            "input_query", help="Input OverpassQL query or path to .overpassql file"
        )
        # parser.add_argument("output_file", help="Output XLSX")

        # # @see https://stackoverflow.com/questions/41669690/how-to-overcome-the-limit-of-hyperlinks-in-excel
        # parser.add_argument(
        #     "--hiperlink",
        #     help="Add hiperlink to column names if they have non-empty value. "
        #     "alredy are mached with each other. "
        #     "Use '||' to deparate colum name from the URL. "
        #     "Add {value} as part of the URL for placeholder of external link. "
        #     "Accept multiple values. "
        #     "Example: "
        #     "--pivot-key-main='colum_name||http://example.com/page/{value}'",
        #     dest="hiperlink",
        #     nargs="?",
        #     action="append",
        # )

        return parser.parse_args()

    def execute_cli(self, pyargs, stdin=STDIN, stdout=sys.stdout, stderr=sys.stderr):
        query = pyargs.input_query
        if pyargs.input_query.endswith(".overpassql"):
            with open(pyargs.input_query, "r") as file:
                query = file.read()

        # print(query)
        # print('')
        # print('')

        result_str = overpassql2osmf(
            query,
        )
        print(result_str)
        # with open(pyargs.output_file, "w") as file:
        #     file.write(result_str)

        return self.EXIT_OK


def overpassql2osmf(input_query: str):
    """overpassql2osmf
    @see https://xlsxwriter.readthedocs.io/example_pandas_autofilter.html

    Args:
        input_query (str): Input CSV file
        output_file (str): Output XLSX
    """
    payload = {"data": input_query}
    r = requests.post(OVERPASS_INTERPRETER, data=payload)

    return r.text


def parse_argument_values(arguments: list, delimiter: str = "||") -> dict:
    if not arguments or len(arguments) == 0 or not arguments[0]:
        return None

    result = {}
    for item in arguments:
        if item.find(delimiter) > -1:
            _key, _val = item.split(delimiter)
            result[_key] = _val
        else:
            result[_key] = True
    return result


def exec_from_console_scripts():
    main = Cli()
    args = main.make_args()
    main.execute_cli(args)


if __name__ == "__main__":
    cli_main = Cli()
    args = cli_main.make_args()
    cli_main.execute_cli(args)
