#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

pwd
echo "HIHIH"


TEAMID=`md5sum README.md | cut -d' ' -f 1`
docker kill $(docker ps -q)
docker rm $(docker ps -a -q)
docker build . -t $TEAMID
docker run -v $(pwd)/src/service/flaskr.db:/service/flaskr.db -p 80:80 -p 8080:8080 -t $TEAMID 
