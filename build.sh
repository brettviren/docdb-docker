#!/bin/bash

namespace=$1 ; shift
if [ -z "$namespace" ] ; then
    echo "usage: $0 <namespace>"
    exit 1
fi

srcdir=$(dirname $(readlink -f $BASH_SOURCE))

do_build_image () {
    local name=$1 ; shift
    local fullname="$namespace/$name"
    docker build -t $fullname $srcdir/docdb-$name
}

#do_build_image daemons
do_build_image mysql
do_build_image storage



