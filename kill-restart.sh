#/bin/bash

lsof -n -iTCP:80  -sTCP:LISTEN -n -l -P | grep 'LISTEN' | awk '{print $2}' | xargs kill -9
lsof -n -iTCP:8080  -sTCP:LISTEN -n -l -P | grep 'LISTEN' | awk '{print $2}' | xargs kill -9
sudo ./run.sh
