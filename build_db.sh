#!/bin/bash

# Settings
AST_DIR=`pwd`/"runtime/ast"
DB_DIR=`pwd`/"runtime"
DB_BIN=`pwd`/ast/build_db_from_ast.py

# Build db
python ${DB_BIN} -a ${AST_DIR}/kernel/sched/core.c.ast.json -o ${DB_DIR}/sched.json -d
