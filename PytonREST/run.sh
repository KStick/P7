#!/bin/bash

if [[ "$OSTYPE" == "linux-gnu" ]]; then
	export FLASK_APP=RestApi.py
	flask initdb
	flask run
elif [[ "$OSTYPE" == "win32" ]]; then
	set FLASK_APP=RestApi.py
	flask initdb
	xterm -e flask run
	xterm -e C:\Program Files\httpd-2.4.27-x64-vc14\Apache24\bin\httpd.exe
fi
