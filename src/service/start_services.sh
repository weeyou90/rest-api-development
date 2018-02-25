#!/bin/bash

apachectl start
ls
cd src/service

export FLASK_APP=src/service/app.py
python ./app.py

