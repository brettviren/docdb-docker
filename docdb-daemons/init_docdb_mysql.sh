#!/bin/bash

if [ ! -f /.docdb_mysql_init ] ; then
    echo "DocDB MySQL already initialized!"
    exit 0
fi

dbname=${DOCDB_DATABASE:-DocDB}


cat <<EOF >/.docdb_mysql_init

EOF

mysql -u root -p
mysql> show databases;
mysql> use mysql;
mysql> select * from user;
mysql> delete from user where user="";
mysql> create database SomeDocDB;
mysql> grant select on SomeDocDB.* to docdbro@localhost identified by "read only password";
mysql> grant select on SomeDocDB.* to docdbro@mydocs.fnal.gov identified by "read only password";
mysql> grant select,insert,update,delete on SomeDocDB.* to docdbrw@mydocs.fnal.gov identified by "read write password";
mysql> grant select,insert,update,delete on SomeDocDB.* to docdbrw@localhost identified by "read write password";
mysql> grant ALL on SomeDocDB.* to docdbadm@localhost identified by "database owner password";
mysql> grant ALL on SomeDocDB.* to docdbadm@mydocs.fnal.gov identified by "database owner password";
mysql> quit
