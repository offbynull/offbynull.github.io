#!/bin/bash

# github is set to read page contents from /docs

# build in ./build
npm run-script build
# in ./docs, delete all files except ./docs/data
# -depth option: https://unix.stackexchange.com/q/258057
old_docs_dir=$(mktemp -d -t docs-XXXXXXXXXX)
cp -a docs $old_docs_dir
find docs/* -depth -name "*" -print | grep -v "^docs/data" | xargs -n1 rm -rf
# using tar, recursive copy ./build to ./docs except for ./build/data
tar --exclude='data' -cvf - -C build . | tar -C docs -xvf -
# remove ./build
old_build_dir=$(mktemp -d -t build-XXXXXXXXXX)
mv build $old_build_dir