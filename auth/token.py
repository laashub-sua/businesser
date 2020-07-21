from flask import request

from config import config_data
from exception import MyServiceException


def do_auth():
    config_token = config_data['application']["security"]["token"]
    if "token" not in request.headers:
        raise MyServiceException('request failure, because miss the token in request header')
    request_header_token = request.headers["token"]
    if not request_header_token == config_token:
        raise MyServiceException('request failure, because miss the token in request header')
