#!/bin/bash

if [[ "$OSTYPE" == "linux-gnu" ]]; then
	export FLASK_APP=RestApi.py
	flask initdb
	flask run
elif [[ "$OSTYPE" == "win32" ]]; then
	set FLASK_APP=RestApi.py
	flask initdb
	flask run
fi
