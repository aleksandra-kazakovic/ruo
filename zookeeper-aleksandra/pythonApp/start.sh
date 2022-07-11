#!/bin/bash
path=`pwd`
mysql_init_path="$path/mysql/init"
mysql_storage_path="$path/mysql/storage"
docker run --env="MYSQL_ROOT_PASSWORD=kazak" \
    -p 3306:3306 \
    -v mysql_init_path:/docker-entrypoint-initdb.d  \
    -v mysql_storage_path:/var/lib/mysql \
    -d  \
    mysql:latest

