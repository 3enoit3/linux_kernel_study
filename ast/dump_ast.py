#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Dump ast"""

# inspired by from https://gist.github.com/anonymous/2503232
# inspired by http://eli.thegreenplace.net/2011/07/03/parsing-c-in-python-with-clang/

import sys
import argparse
import unittest
import logging
import clang.cindex
import json
import os

def get_path(cmd):
    return os.path.normpath(os.path.join(cmd.directory, cmd.filename))

def build_tu(index, cmd):
    args = [a for a in cmd.arguments if not a.startswith("-f") and not a.startswith("-m") and not a.startswith("-O")][1:-3]
    tu = index.parse(get_path(cmd), args=args)
    return tu

def get_includes(tu):
    root = { "file":tu.spelling, "includes":[] }
    path = [root]
    for f in tu.get_includes():
        node = { "file":f.include.name, "includes":[] }
        while f.depth < len(path):
            path.pop()
        path[-1]["includes"].append(node)
        if f.depth >= len(path):
            path.append(node)
    return root

def get_ast(tu):
    def is_valid_type(t):
        '''used to check if a cursor has a type'''
        return t.kind != clang.cindex.TypeKind.INVALID

    def qualifiers(t):
        '''set of qualifiers of a type'''
        q = set()
        if t.is_const_qualified(): q.add('const')
        if t.is_volatile_qualified(): q.add('volatile')
        if t.is_restrict_qualified(): q.add('restrict')
        return q

    def get_type(t):
        node = { "kind": str(t.kind) }

        extra = qualifiers(t)
        if extra:
            node["qualifiers"] = list(extra)

        if is_valid_type(t.get_pointee()):
            node["points_to"] = get_type(t.get_pointee())

        return node

    def get_node(cursor):
        node = { "kind": str(cursor.kind),
                "spelling": cursor.spelling,
                "displayname": cursor.displayname,
                "location": str(cursor.location) }

        if is_valid_type(cursor.type):
            node["type"] = get_type(cursor.type)
            canonical = get_type(cursor.type.get_canonical())
            if canonical != node["type"]:
                node["canonical"] = canonical

        children = []
        for c in cursor.get_children():
            children.append( get_node(c) )
        if children:
            node["children"] = children

        return node

    return get_node(tu.cursor)

def build_output_path(cmd, output_dir):
    path = get_path(cmd)
    root = os.getcwd() + "/"

    if path.startswith(root):
        return os.path.join(output_dir, path[len(root):])
    else:
        return os.path.join(output_dir, path)

def save_json(json_path, tree):
    json_dir = os.path.dirname(json_path)
    if not os.path.isdir(json_dir):
        os.makedirs(json_dir)

    with open(json_path, "w") as json_file:
        json_file.write(json.dumps(tree, indent=2))


def dump_asts(db_path, ast_dir):
    # initialize clang
    clang.cindex.Config.set_library_file('/usr/lib/x86_64-linux-gnu/libclang-7.so.1')
    index = clang.cindex.Index.create()

    db_dir = os.path.dirname(os.path.abspath(db_path))
    db = clang.cindex.CompilationDatabase.fromDirectory(db_dir)

    # parse all known files
    for cmd in db.getAllCompileCommands():
        logging.debug("parsing %s ..", get_path(cmd))

        # parse file
        tu = build_tu(index, cmd)

        # create tree
        tree = { 'unit': tu.spelling,
                 'includes': get_includes(tu),
                 'ast': get_ast(tu)
                }

        # save as json
        json_path = build_output_path(cmd, ast_dir) + ".ast.json"
        logging.debug("writting %s ..", json_path)
        save_json(json_path, tree)

def main():
    """Entry point"""

    # Parse options
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true", default=False,
                        help="show debug information")
    parser.add_argument("-c", "--compile_db", action="store",
                        help="path for compile_commands.json")
    parser.add_argument("-o", "--output_dir", action="store", default=".",
                        help="directory for generated asts")
    args = parser.parse_args()

    # Configure debug
    if args.debug:
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
        logging.debug("Enabled debug logging")

    # Run
    dump_asts(args.compile_db, args.output_dir)

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
