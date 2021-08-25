#!/bin/bash
#                                                                  this is for development and debugging the code not for deployment
export FLASK_APP=app.py
export FLASK_DEBUG=true
export FLASK_ENV=development
export FLASK_DEBUG=1

flask run
