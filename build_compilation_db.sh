#!/bin/bash

# Settings
KERNEL_DIR="runtime/kernel/linux"
BUILD_TARGET="kernel/"

BEAR_DIR="runtime/bear"
BEAR="${BEAR_DIR}/Bear/bear/bear"
LIBEAR="${BEAR_DIR}/Bear/libear/libear.so"

COMPILATION_DB="runtime/compile_commands.json"

# Install bear if needed
if [ ! -f "${BEAR}" ]; then
    # Isolate in its own directory
    mkdir -p ${BEAR_DIR}
    pushd ${BEAR_DIR}

    # Install source
    git clone --depth 1 https://github.com/rizsotto/Bear
    cd Bear

    # Build
    cmake .
    make all

    popd
fi

# Build compilation database
make -C ${KERNEL_DIR} clean
${BEAR} -o ${COMPILATION_DB} -l `pwd`/${LIBEAR} make -C ${KERNEL_DIR} -j `getconf _NPROCESSORS_ONLN` ${BUILD_TARGET}
