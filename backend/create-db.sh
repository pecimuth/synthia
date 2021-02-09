#!/bin/bash
# the server must be running already
export FLASK_ENV=development
export FLASK_APP=web
./env/Scripts/python -m flask create-db
