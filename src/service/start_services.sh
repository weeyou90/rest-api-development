#!/bin/bash

apachectl start
cd service
sqlite3 -line flaskr.db "insert into diary_entries values (1,2,3,4,5,6)"
sqlite3 -line flaskr.db "select * from diary_entries"

export FLASK_APP=/service/app.py
python ./app.py
