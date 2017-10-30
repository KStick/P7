#!/bin/bash

if [[ "$OSTYPE" == "linux-gnu" ]]; then
	export FLASK_APP=RestApi.py
	flask initdb
	flask run
elif [[ "$OSTYPE" == "win32" ]]; then
	bash -c "set FLASK_APP=RestApi.py"
	bash -c "flask initdb"
	bash -c "xterm -e flask run"
	bash -c "xterm -e C:\Program Files\httpd-2.4.27-x64-vc14\Apache24\bin\httpd.exe"
fi
