#!/bin/bash

apachectl start
ls
cd /service

export FLASK_APP=/service/app.py
python ./app.py

