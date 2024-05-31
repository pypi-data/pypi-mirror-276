#!/usr/bin/env python3
# ==============================================================================
#
#          FILE:  geojsonconcat.py
#
#         USAGE:  geojsonconcat --help
#                 ./src/gisconflation/geojsonconcat.py --help
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
#       CREATED:  2023-05-31 11:23 BRT
# ==============================================================================

import argparse
import csv

# import csv
# import dataclasses
import json

# import re
import sys

__VERSION__ = "1.0.0"

PROGRAM = "geojsonconcat"

# https://www.rfc-editor.org/rfc/rfc7946
# https://www.rfc-editor.org/rfc/rfc8142.html
DESCRIPTION = """
------------------------------------------------------------------------------
Concat 2 or more GeoJSON files into GeoJSON (RFC 7946) or
GeoJSON Text Sequences (RFC 8142)

@TODO for input files know to be GeoJSONSeq, read line by line

------------------------------------------------------------------------------
""".format(
    __file__
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

    {0} input-a.geojson input-b.geojson > merged-a+b.geojson

    {0} --format-output=RFC8142 input-a.geojson input-b.geojson \
> merged-a+b.geojsonseq

------------------------------------------------------------------------------
                            EXEMPLŌRUM GRATIĀ
------------------------------------------------------------------------------
""".format(
    PROGRAM
)

STDIN = sys.stdin.buffer

# MATCH_EXACT = 1
# MATCH_NEAR = 3


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
        """make_args

        Args:
            hxl_output (bool, optional): _description_. Defaults to True.
        """
        parser = argparse.ArgumentParser(
            prog=PROGRAM,
            description=DESCRIPTION,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=__EPILOGUM__,
        )

        parser.add_argument(
            "inputs", help="One or more input GeoJSON/GeoJSONSeq", nargs="+"
        )
        # parser.add_argument("geodataset_b", help="GeoJSON dataset 'B'")

        # # @TODO maybe implement GeoJSONSeq
        # parser.add_argument("input", help="Input GeoJSON / GeoJSONSeq. Use - for stdin")
        # # parser.add_argument("geodataset_b", help="GeoJSON dataset 'B'")

        # @see https://stevage.github.io/ndgeojson/
        # @see https://datatracker.ietf.org/doc/html/rfc8142
        parser.add_argument(
            "--format-output",
            help="Output format GeoJSON (RFC7946) or GeoJSON Text Sequences (RFC 8142)",
            dest="format_output",
            default="RFC7946",
            required=False,
            choices=["RFC7946", "RFC8142"],
            # choices=["auto", "geojson", "geojsonseq"],
            nargs="?",
        )

        return parser.parse_args()

    def execute_cli(self, pyargs, stdin=STDIN, stdout=sys.stdout, stderr=sys.stderr):
        gconcat = GeoJSOnConcater(
            inputs=pyargs.inputs,
            # geodataset_b=pyargs.geodataset_b,
            # skip_invalid_geometry=True,
        )
        # print("TODO")

        gconcat.output()
        # gmerger.debug()
        return self.EXIT_OK


# class GeoJSONMerger:
class GeoJSOnConcater:
    def __init__(self, inputs: list, output_format: str = None) -> None:
        self.inputs = inputs
        self.output_format = output_format

    def _loader_temp(self, input_ptr: str):
        # @TODO make this efficient for very large files
        data = None
        if input_ptr == "-":
            temp = []
            for line in sys.stdin:
                # temp.append(line.strip())
                temp.append(line.rstrip())
                # temp.append(line)

            data = "\n".join(temp)
        else:
            with open(input_ptr, "r") as _file:
                data = _file.read()
            # pass

        return data

    def debug(self):
        # print("todo")
        print(self.statistics)

    def output(self):
        # @TODO keep other metadata at top level, if exist

        if self.output_format != "RFC8142":
            print('{"type": "FeatureCollection", "features": [')

        count_files = len(self.inputs)

        for infile in self.inputs:
            # print("TODO", infile)

            # @TODO optimize if know upfront is GeoJSONseq (maybe file extension)
            infile_str = self._loader_temp(infile)
            infile_obj = json.loads(infile_str)

            if "features" not in infile_obj:
                raise SyntaxError(f"File {infile} not GeoJSON. Must have features")

            count_files -= 1
            count_items_now = len(infile_obj["features"])

            for item in infile_obj["features"]:
                count_items_now -= 1
                line_str = json.dumps(item, ensure_ascii=False)
                if self.output_format != "RFC8142" and (
                    count_items_now > 0 or count_files > 0
                ):
                    line_str += ","

                # @TODO deal with geojsonseq RS on this part

                # https://www.rfc-editor.org/rfc/rfc8142
                if self.output_format == "RFC8142":
                    print(f"\x1e{line_str}\n", sep="", end="")
                else:
                    print(line_str)

        # count = len(self.out_dict.keys())
        # for _key, item in self.out_dict.items():
        #     count -= 1
        #     line_str = json.dumps(item, ensure_ascii=False)
        #     if count > 0:
        #         line_str += ","
        #     print(line_str)
        if self.output_format != "RFC8142":
            print("]}")

        # print("")
        # self.debug()


# https://stackoverflow.com/questions/3952132/how-do-you-dynamically-identify-unknown-delimiters-in-a-data-file
def get_delimiter(file_path: str, encoding="utf-8") -> str:
    with open(file_path, "r", encoding=encoding) as csvfile:
        delimiter = str(csv.Sniffer().sniff(csvfile.read()).delimiter)
        return delimiter


def exec_from_console_scripts():
    main = Cli()
    args = main.make_args()
    main.execute_cli(args)


if __name__ == "__main__":
    main = Cli()
    args = main.make_args()
    main.execute_cli(args)
