#!/bin/bash

namespace=$1 ; shift
if [ -z "$namespace" ] ; then
    echo "usage: start.sh <namespace>"
    exit 1
fi

do_stop_containers () {
    local name=$1 ; shift
    local fullname="$namespace/$name"
    for dcid in $(docker ps -a|grep $fullname|grep ' Up '| awk '{print $1}')
    do
	docker stop $dcid
    done
}


do_stop_containers daemons
do_stop_containers storage

