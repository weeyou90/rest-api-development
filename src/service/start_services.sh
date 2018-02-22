#!/bin/bash

apachectl start
# cd service
# gunicorn --config=gunicorn.py app:app
# cd ..
python /service/app.py
# run -v ${pwd}/service:/opt/service/ -i -t examp