#!/bin/bash

export FLASK_APP=RestApi.py
flask initdb
flask run
