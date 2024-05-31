#!/usr/bin/env python3
# ==============================================================================
#
#          FILE:  geojsonmerger.py
#
#         USAGE:  geojsonmerger --help
#                 ./src/gisconflation/geojsonmerger.py --help
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
#       VERSION:  v0.1.0
#       CREATED:  2023-04-28 14:17 BRT
# ==============================================================================

import argparse
import csv

# import csv
# import dataclasses
import json
import re
import sys
from csv2geojson.csv2geojson import _zzz_format_phone_br

from gisconflation.util import AttributesEditor

# import logging
# from typing import List, Type

# from .util import AttributesEditor, parse_argument_values

# geojsonmerger tests/temp/dataset_a.geojson tests/temp/dataset_b.geojson
# geojsonmerger tests/temp/dataset_a.geojson tests/temp/dataset_b.geojson > tests/temp/dataset_a+b.geojson

# geojsonmerger tests/temp/dataset_a.geojson /workspace/git/fititnt/openstreetmap-vs-dados-abertos-brasil/data/tmp/DATASUS-tbEstabelecimento.csv
# geojsonmerger tests/temp/dataset_a.geojson /workspace/git/fititnt/openstreetmap-vs-dados-abertos-brasil/data/tmp/DATASUS-tbEstabelecimento.csv > tests/temp/dataset_csv_a+b.geojson
# geojsonmerger tests/temp/iede.rs.gov.br_Hospitais-no-RS_v2.geojson /workspace/git/fititnt/openstreetmap-vs-dados-abertos-brasil/data/tmp/DATASUS-tbEstabelecimento.csv > tests/temp/iede.rs.gov.br_Hospitais-no-RS_v2_plusmetadata.geojson

# other repo
# geojsonmerger data/tmp/DATASUS-tbEstabelecimento__RS.geojson data/tmp/ReceitaFederal_CNPJ_Estabelecimentos__RS_2023-05-09.csv
# geojsonmerger data/tmp/DATASUS-tbEstabelecimento__RS.geojson data/tmp/ReceitaFederal_CNPJ_Estabelecimentos__RS_2023-05-09.csv

__VERSION__ = "0.1.0"

PROGRAM = "geojsonmerger"
DESCRIPTION = """
------------------------------------------------------------------------------
[DRAFT] GeoJSON simple merger

Merge extra attributes from an GeoJSON (likely the one with more metadata, but
not accurate geometry) into another GeoJSON.

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

        parser.add_argument("geodataset_a", help="GeoJSON dataset 'A'")
        parser.add_argument("geodataset_b", help="GeoJSON dataset 'B'")

        # # @TODO maybe implement GeoJSONSeq
        # parser.add_argument("input", help="Input GeoJSON / GeoJSONSeq. Use - for stdin")
        # # parser.add_argument("geodataset_b", help="GeoJSON dataset 'B'")

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

        # normalize_prop = True
        # skip_invalid_geometry = True

        # # raise ValueError(parse_argument_values(pyargs.value_fixed))
        # # print(parse_argument_values(pyargs.value_fixed))

        # gitem = GeoJSONItemEditor(
        #     rename_attr=parse_argument_values(pyargs.rename_attr),
        #     value_fixed=parse_argument_values(pyargs.value_fixed),
        #     value_name_place=pyargs.value_name_place,
        #     normalize_prop=normalize_prop,
        #     skip_invalid_geometry=skip_invalid_geometry,
        # )
        # gedit = GeoJSONFileEditor(pyargs.input, gitem)
        # gedit.output()

        # skip_invalid_geometry: True

        # # geodiff.debug()
        gmerger = GeoJSONMerger(
            geodataset_a=pyargs.geodataset_a,
            geodataset_b=pyargs.geodataset_b,
            # skip_invalid_geometry=True,
        )
        # print("TODO")

        gmerger.output()
        # gmerger.debug()
        return self.EXIT_OK


class GeoJSONMerger:
    def __init__(self, geodataset_a, geodataset_b) -> None:
        self.geodataset_a = geodataset_a
        self.geodataset_b = geodataset_b

        # @TODO make it flexible
        self.key_a = "ref:CNES"
        self.key_b = "CO_CNES"
        self.map_b = {
            "NU_CNPJ": "ref:vatin",
            "NU_CNPJ_MANTENEDORA": "operator:ref:vatin",
            "CO_CEP": "addr:postcode",
            "NO_EMAIL": "email",
            "NU_TELEFONE": "phone",
        }
        self.map_b_callback = {
            "NU_CNPJ": lambda x: f"BR{x}",
            "NU_CNPJ_MANTENEDORA": lambda x: f"BR{x}",
            "CO_CEP": lambda x: re.sub(r"(\d{5})(\d{3})", r"\1-\2", x),
            "NO_EMAIL": lambda x: x.lower(),
            "NU_TELEFONE": _zzz_format_phone_br,
        }

        self.in_a = []
        self.in_b = []
        self.out = []
        self.out_dict = {}

        self.statistics = {
            "a_items": 0,
            "a_items_valid": 0,
            "b_items": 0,
            "b_items_valid": 0,
            "ab_match": 0,
        }

        self._init_a()
        self._init_b()

    def _init_a(self) -> None:
        a_str = self._loader_temp(self.geodataset_a)

        a_data = json.loads(a_str)
        for item in a_data["features"]:
            self.statistics["a_items"] += 1
            if not "properties" in item or not item["properties"]:
                raise SyntaxError(item)

            if not self.key_a in item["properties"]:
                raise SyntaxError([self.key_a, item])

            key_active = str(item["properties"][self.key_a])
            if key_active in self.out_dict:
                # Improve this err handling
                print(f"Repeated value {key_active}")

            self.statistics["a_items_valid"] += 1
            self.out_dict[key_active] = item
            # print(item)

    def _init_b(self) -> None:
        # @TODO refactor this part
        if self.geodataset_b.lower().endswith((".csv", ".tsv", ".tab")):
            encoding = "latin-1"
            # _delimiter = get_delimiter(self.geodataset_b, encoding)
            _delimiter = ";"

            with open(self.geodataset_b, "r", encoding=encoding) as csvfile:
                reader = csv.DictReader(csvfile, delimiter=_delimiter)
                aedit = AttributesEditor(normalize_prop=True)
                for row in reader:
                    self.statistics["b_items"] += 1
                    if not self.key_b in row:
                        raise SyntaxError([self.key_b, item])

                    key_active = str(row[self.key_b])

                    self.statistics["b_items_valid"] += 1
                    if key_active not in self.out_dict:
                        continue
                    self.statistics["ab_match"] += 1

                    _props = self.out_dict[key_active]["properties"]
                    for _key, _val in row.items():
                        # @TODO allow some filtering
                        # _props[_key] = _val

                        if self.map_b_callback and _key in self.map_b_callback:
                            if _val:
                                _val = self.map_b_callback[_key](_val)

                        if self.map_b and _key in self.map_b:
                            _newkey = self.map_b[_key]
                            _props[_newkey] = _val
                        else:
                            _props[f"__b_{_key}"] = _val

                    _props2 = aedit.edit(_props)

                    # self.out_dict[key_active]["properties"] = _props
                    self.out_dict[key_active]["properties"] = _props2
                    # print(row)
                    # print(row['first_name'], row['last_name'])

            return True

        b_str = self._loader_temp(self.geodataset_b)

        b_data = json.loads(b_str)

        for item in b_data["features"]:
            self.statistics["b_items"] += 1
            if (
                not "properties" in item
                or not item["properties"]
                or not isinstance(item["properties"], dict)
            ):
                continue
                # raise SyntaxError(item)

            if not self.key_b in item["properties"]:
                raise SyntaxError([self.key_b, item])

            key_active = str(item["properties"][self.key_b])

            self.statistics["b_items_valid"] += 1

            if key_active not in self.out_dict:
                continue

            self.statistics["ab_match"] += 1
            # raise ValueError('deu')
            # print(key_active, type(key_active))
            # print(self.out_dict[key_active])
            # print('')
            # print(self.out_dict[key_active]["properties"])
            # print(item)

            _props = self.out_dict[key_active]["properties"]

            for _key, _val in item["properties"].items():
                # @TODO allow some filtering
                # _props[_key] = _val
                _props[f"__b_{_key}"] = _val

            # _props = {
            #     **self.out_dict[key_active]["properties"],
            #     **item["properties"][self.key_b],
            # }
            # self.out_dict[key_active]["properties"].update(
            #     item["properties"][self.key_b]
            # )
            self.out_dict[key_active]["properties"] = _props

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
        print('{"type": "FeatureCollection", "features": [')
        count = len(self.out_dict.keys())
        for _key, item in self.out_dict.items():
            count -= 1
            line_str = json.dumps(item, ensure_ascii=False)
            if count > 0:
                line_str += ","
            print(line_str)
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
