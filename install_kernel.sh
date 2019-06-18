#!/bin/bash

# from https://wiki.ubuntu.com/KernelTeam/GitKernelBuild

# Install general dependencies
sudo apt-get install git build-essential kernel-package fakeroot libncurses5-dev libssl-dev ccache bison flex libelf-dev

# Install clang, from http://apt.llvm.org/

# for ubuntu trusty, add the following lines to /etc/apt/sources.list:
#   deb http://apt.llvm.org/trusty/ llvm-toolchain-trusty main
#   deb-src http://apt.llvm.org/trusty/ llvm-toolchain-trusty main
#   # 7
#   deb http://apt.llvm.org/trusty/ llvm-toolchain-trusty-7 main
#   deb-src http://apt.llvm.org/trusty/ llvm-toolchain-trusty-7 main
#   # 8
#   deb http://apt.llvm.org/trusty/ llvm-toolchain-trusty-8 main
#   deb-src http://apt.llvm.org/trusty/ llvm-toolchain-trusty-8 main
#   # gcc backport
#   deb http://ppa.launchpad.net/ubuntu-toolchain-r/test/ubuntu trusty main

sudo apt-get install clang-7 clang-tools-7 lldb-7 lld-7
sudo pip install clang

# Isolate in its own directory
mkdir -p runtime/kernel
cd runtime/kernel

# Install sources
git clone --depth 1 git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git
cd linux

# Create .config
yes '' | make oldconfig
# make menuconfig for extra settings

# Ready to build: make -j `getconf _NPROCESSORS_ONLN` deb-pkg LOCALVERSION=-custom
