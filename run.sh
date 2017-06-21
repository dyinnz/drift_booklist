#!/bin/bash
export FLASK_APP=drift_app
pip3 install -e .
flask run
