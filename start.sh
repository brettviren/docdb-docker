#!/bin/bash

usage () {
    echo "usage: start.sh <namespace> <sshpubkeyfile>"
    exit 1
}

namespace=$1 ; shift
if [ -z "$namespace" ] ; then usage; fi

keyfile=$1 ; shift
if [ -z "$keyfile" ] ; then usage; fi


run_storage () {

    conname="${namespace}_storage"

    if docker inspect $conname >/dev/null 2>&1 ; then
	if [ -n "$(docker ps -a|grep $conname | grep ' Up ')" ] ; then
	    echo "Container already up: $conname"
	else
	    echo "Starting stopped container: $conname"
	    docker start $conname
	fi
	docker ps $conname
	return
    fi

    docker run -d -P --name ${namespace}_storage \
	-v /var/lib/docdb -v /var/lib/mysql -v /var/log \
	-e AUTHORIZED_KEYS="$(cat $keyfile)" \
	${namespace}/storage

}
run_daemons () {

    conname="${namespace}_daemons"

    if docker inspect $conname >/dev/null 2>&1 ; then
	if [ -n "$(docker ps -a|grep $conname | grep ' Up ')" ] ; then
	    echo "Container already up: $conname"
	else
	    echo "Starting stopped container: $conname"
	    docker start $conname
	fi
	docker ps $conname
	return
    fi

    docker run -d -P --name ${namespace}_daemons \
	--volumes-from ${namespace}_storage \
	-e AUTHORIZED_KEYS="$(cat $keyfile)" \
	${namespace}/daemons

}


run_storage
run_daemons
