#!/bin/bash

# Install dependencies
sudo apt-get install doxygen

# Isolate in its own directory
mkdir -p runtime/doxygen
cp doxygen/Doxyfile runtime/doxygen
cd runtime/doxygen

# Build
doxygen
