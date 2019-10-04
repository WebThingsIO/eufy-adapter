#!/bin/bash

set -e

version=$(grep version package.json | cut -d: -f2 | cut -d\" -f2)

# Clean up from previous releases
rm -rf *.tgz package SHA256SUMS

# Prep new package
mkdir package

# Put package together
cp -r pkg LICENSE manifest.json package.json *.py README.md requirements.txt setup.cfg package/
find package -type f -name '*.pyc' -delete
find package -type d -empty -delete

# Generate checksums
cd package
find . -type f -exec sha256sum {} \; >> SHA256SUMS
cd -

# Make the tarball
tar czf "eufy-adapter-${version}.tgz" package
