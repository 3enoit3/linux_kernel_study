#!/bin/bash

# Settings
KERNEL_DIR=`pwd`/"runtime/kernel/linux"
COMPILATION_DB=`pwd`/"runtime/compile_commands.json"
AST_DIR=`pwd`/"runtime/ast"
AST_BIN=`pwd`/ast/dump_ast.py

# Prepare directory
rm -rf ${AST_DIR}
mkdir -p ${AST_DIR}

# Build ast
cd ${KERNEL_DIR}
python ${AST_BIN} -c ${COMPILATION_DB} -o ${AST_DIR} -d
