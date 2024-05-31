#!/usr/bin/env python3
# ==============================================================================
#
#          FILE:  geojsonedit.py
#
#         USAGE:  geojsonedit --help
#                 ./src/gisconflation/geojsonedit.py --help
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
#       CREATED:  2023-04-28 14:17 BRT
# ==============================================================================

import argparse

# import csv
# import dataclasses
import json
import sys

# import logging
from typing import List, Type

from .util import AttributesEditor, parse_argument_values

# from haversine import haversine, Unit

# # from shapely.geometry import Polygon, Point
# from shapely.geometry import Polygon
# from xml.sax.saxutils import escape


__VERSION__ = "0.5.0"

PROGRAM = "geojsonedit"
DESCRIPTION = """
------------------------------------------------------------------------------
GeoJSON / GeoJSONSeq command line editor

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

        # @TODO maybe implement GeoJSONSeq
        parser.add_argument("input", help="Input GeoJSON / GeoJSONSeq. Use - for stdin")
        # parser.add_argument("geodataset_b", help="GeoJSON dataset 'B'")

        parser.add_argument(
            "--format-output",
            help="Path to output file",
            dest="format_output",
            default="auto",
            required=False,
            choices=["auto", "geojson", "geojsonseq"],
            nargs="?",
        )

        edit = parser.add_argument_group("Change properties from each item")

        edit.add_argument(
            "--rename-attribute",
            help="Rename attribute (if exist). "
            "Use '||' to divide the source key and target key. "
            "Accept multiple values. "
            "Example: "
            "--rename-attribute='NAME|||name' --rename-attribute='CITY|||addr:city'",
            dest="rename_attr",
            nargs="?",
            action="append",
        )

        # Old versions of csv2geojson uses only one |
        edit.add_argument(
            "--value-fixed",
            help="Define a fixed string for every value of a column, "
            "For multiple, use multiple times this parameter. "
            "Source vs destiny column must be divided by |||. "
            "Example: <[ --value-fixed='source|||BR:DATASUS' ]>",
            dest="value_fixed",
            nargs="?",
            # type=lambda x: x.split("||"),
            action="append",
            default=None,
        )

        edit.add_argument(
            "--value-norm-name-place",
            help="Column to normalize value (strategy: name of place). "
            "Accept multiple options. Example: "
            "--value-norm-name-place='name' --value-norm-name-place='alt_name'",
            dest="value_name_place",
            nargs="?",
            # type=lambda x: x.split("||"),
            action="append",
            default=None,
        )

        filter = parser.add_argument_group("Options for filter input items completely")

        return parser.parse_args()

    def execute_cli(self, pyargs, stdin=STDIN, stdout=sys.stdout, stderr=sys.stderr):
        # logger = logging.getLogger()
        # logger.setLevel(logging.INFO)
        # if pyargs.outlog:
        #     fh = logging.FileHandler(pyargs.outlog)
        #     logger.addHandler(fh)
        # else:
        #     ch = logging.StreamHandler()
        #     logger.addHandler(ch)

        normalize_prop = True
        skip_invalid_geometry = True

        # raise ValueError(parse_argument_values(pyargs.value_fixed))
        # print(parse_argument_values(pyargs.value_fixed))

        gitem = GeoJSONItemEditor(
            rename_attr=parse_argument_values(pyargs.rename_attr),
            value_fixed=parse_argument_values(pyargs.value_fixed),
            value_name_place=pyargs.value_name_place,
            normalize_prop=normalize_prop,
            skip_invalid_geometry=skip_invalid_geometry,
        )
        gedit = GeoJSONFileEditor(pyargs.input, gitem)
        gedit.output()

        # geodiff.debug()
        return self.EXIT_OK


# ./src/gisconflation/geojsonedit.py tests/data/geojson-simple.geojson
# cat tests/data/geojson-simple.geojson | ./src/gisconflation/geojsonedit.py -
# ./src/gisconflation/geojsonedit.py tests/data/geojson-seq.geojsonl
class GeoJSONFileEditor:
    """GeoJSONEditor

    @TODO implement read line-by-line large files (in special GeoJSONSeq)
    """

    def __init__(self, input_ptr: str, gitem: Type["GeoJSONItemEditor"]) -> None:
        self.gitem = gitem
        self.inputdata = self._loader_temp(input_ptr)
        # pass

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

    def output(self):
        json_data = json.loads(self.inputdata)
        if not json_data or "features" not in json_data:
            raise SyntaxError("bad input data")

        result = {"features": []}
        for item in json_data["features"]:
            edited_item = self.gitem.edit(item)
            if edited_item is not False:
                result["features"].append(edited_item)

        # print(self.inputdata)
        # print(json_data)

        # @TODO keep other metadata at top level, if exist
        print('{"type": "FeatureCollection", "features": [')
        count = len(json_data["features"])
        for item in json_data["features"]:
            count -= 1
            line_str = json.dumps(item, ensure_ascii=False)
            if count > 0:
                line_str += ","
            print(line_str)
        print("]}")

        # print(json.dumps(result, ensure_ascii=False))


class GeoJSONItemEditor:
    def __init__(
        self,
        rename_attr: dict = None,
        value_fixed: dict = None,
        value_name_place: list = None,
        normalize_prop: bool = True,
        skip_invalid_geometry: bool = True,
    ) -> None:
        self.rename_attr = rename_attr
        self.normalize_prop = normalize_prop
        self.value_fixed = value_fixed
        self.value_name_place = value_name_place
        self.skip_invalid_geometry = skip_invalid_geometry

        self._attr_editor = AttributesEditor(
            rename_attr=rename_attr,
            value_fixed=value_fixed,
            value_name_place=value_name_place,
            normalize_prop=normalize_prop,
        )

        # print(self.rename_attr)
        # pass

    def edit(self, item: dict):
        # return item
        # print(item)
        result = item

        if self.skip_invalid_geometry:
            if (
                not item
                or not isinstance(item, dict)
                or "geometry" not in item
                or not item["geometry"]
                or "coordinates" not in item["geometry"]
                # or not item["geometry"]["coordinates"]
            ):
                # @TODO make better checks, like if is Type=Point, etc
                return False

        if "properties" in result:
            result["properties"] = self._attr_editor.edit(result["properties"])

            # if self.rename_attr is not None and len(self.rename_attr.keys()) > 0:
            #     for key, val in self.rename_attr.items():
            #         if key in result["properties"]:
            #             result["properties"][val] = result["properties"].pop(key)

            # if self.normalize_prop:
            #     prop_new = {}
            #     # print(result["properties"])
            #     for key, val in sorted(result["properties"].items()):
            #         if isinstance(val, str):
            #             val = val.strip()
            #         if not val:
            #             continue
            #         prop_new[key] = val
            #     result["properties"] = prop_new
        return result


# def parse_argument_values(arguments: list, delimiter: str = "||") -> dict:
#     if not arguments or len(arguments) == 0 or not arguments[0]:
#         return None

#     result = {}
#     for item in arguments:
#         # print('__', item, item.find(delimiter))
#         if item.find(delimiter) > -1:
#             _key, _val = item.split(delimiter)
#             result[_key] = _val
#         else:
#             result[item] = True

#     # print('__f', result)
#     return result


def exec_from_console_scripts():
    main = Cli()
    args = main.make_args()
    main.execute_cli(args)


if __name__ == "__main__":
    main = Cli()
    args = main.make_args()
    main.execute_cli(args)
