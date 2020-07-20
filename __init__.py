import os

from flask import Flask
from flask_cors import CORS

import config
from component import logging

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = os.urandom(24)
CORS(app, supports_credentials=True)
config.do_init()
logging.do_init()
print(str(config.config_data))
