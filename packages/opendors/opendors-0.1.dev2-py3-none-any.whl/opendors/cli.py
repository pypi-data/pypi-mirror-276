# SPDX-FileCopyrightText: 2024 German Aerospace Center (DLR)
# SPDX-FileContributor: Stephan Druskat <stephan.druskat@dlr.de>
#
# SPDX-License-Identifier: MIT

import sys
import argparse
import json

from opendors.model import Corpus


def export_schema(args):
    with open("schema.json", "w") as schema_file:
        if not args.compressed:
            json.dump(Corpus.model_json_schema(), schema_file, indent=4)
        else:
            json.dump(Corpus.model_json_schema(), schema_file)
    print("Exported schema to schema.json.")


class ODLParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("error: %s\n" % message)
        self.print_help()
        sys.exit(2)


def run():
    """
    A simple CLI to interact with he opendors package and model.
    """
    parser = ODLParser(description="opendors utility functions")

    subparsers = parser.add_subparsers(help="Available commands")
    parser_schema = subparsers.add_parser(
        "schema",
        help="Exports the JSON schema for the opendors model to 'schema.json'.",
    )
    parser_schema.add_argument(
        "-c",
        "--compressed",
        help="Export as unindented JSON",
        action="store_true",
        default=False,
    )
    parser_schema.set_defaults(func=export_schema)

    args = parser.parse_args()

    if args.__contains__("func"):
        args.func(args)
    else:
        parser.print_help()
