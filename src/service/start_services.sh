#!/bin/bash

apachectl start
export FLASK_APP=/service/app.py
python -m flask initdb
python /service/app.py
