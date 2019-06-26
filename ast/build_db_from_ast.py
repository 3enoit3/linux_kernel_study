#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Dump ast"""


import sys
import argparse
import unittest
import logging
import json
import os

def xpath(entry, path):
    def is_matching(entry, sub_path):
        if not sub_path:
            return True

        constraints = sub_path.split("&")
        for c in constraints:
            key_value = c.split("=")
            k = key_value[0]
            v = key_value[1]
            if k in entry:
                if entry[k] != v:
                    return False
            else:
                return False
        return True

    def capture(entry, levels):
        if is_matching(entry, levels[0]):
            if len(levels) == 1:
                return [entry]
            else:
                captured = []
                for child in entry["children"]:
                    captured += capture(child, levels[1:])
                return captured
        else:
            return []

    levels = path.split("/")
    return capture(entry, levels)

def collect(ast):
    db = []
    for structs in xpath(ast, "/kind=CursorKind.TRANSLATION_UNIT/kind=CursorKind.STRUCT_DECL"):
        db.append(structs["displayname"])
    return db

def build_db(ast_path, db_path):
    with open(ast_path) as ast_file:
        ast = json.loads(ast_file.read())
    db = collect(ast)
    with open(db_path, "w") as db_file:
        db_file.write(json.dumps(db))

def main():
    """Entry point"""

    # Parse options
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true", default=False,
                        help="show debug information")
    parser.add_argument("-a", "--ast", action="store",
                        help="path for input ast, in json format")
    parser.add_argument("-o", "--output", action="store", default=".",
                        help="path for output db")
    args = parser.parse_args()

    # Configure debug
    if args.debug:
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
        logging.debug("Enabled debug logging")

    # Run
    build_db(args.ast, args.output)

    return 0

if __name__ == "__main__":
    sys.exit(main())

class Tests(unittest.TestCase):
    # pylint: disable=too-many-public-methods
    """Unit tests"""
    # run test suite with
    # python -m unittest <this_module_name_without_py_extension>

    def setUp(self):
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    def test(self):
        """Scenario"""
        self.assertTrue(True is True)
        self.assertEqual(True, True)
