import os

from flask import Flask, make_response
from flask_cors import CORS

import config
from auth import token
from component import flask_blueprint
from component import logging_ as logging
from exception import MyServiceException

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = os.urandom(24)
CORS(app, supports_credentials=True)


@app.errorhandler(500)
def error(e):
    e = e.original_exception
    if isinstance(e, MyServiceException):
        print("e.msg: ", e.msg)
        custom_res = make_response(e.msg)
        custom_res.status = "500"
        return custom_res
    return e


@app.before_request
def do_auth():
    try:
        token.do_auth()
    except Exception as e:
        custom_res = make_response(str(e))
        custom_res.status = "401"
        return custom_res


config.do_init()
logging.do_init()
flask_blueprint.do_init()
logging.info(str(config.config_data))
logging.info(str(app.url_map))
