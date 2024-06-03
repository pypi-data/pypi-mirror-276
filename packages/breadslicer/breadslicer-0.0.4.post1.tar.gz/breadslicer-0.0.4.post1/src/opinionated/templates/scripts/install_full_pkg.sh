#!/bin/sh

for file in ./dist/*.tar.gz ; do
    if [ -e "$file" ] ; then
        pip install "$file[dev]"
    fi
done
