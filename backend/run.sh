#!/bin/bash
export FLASK_ENV=development
export FLASK_APP=web
./env/Scripts/python -m pip install -e .
./env/Scripts/python -m flask run
