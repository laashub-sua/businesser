import json

from flask import Blueprint

from component import rest_form
from exception import MyServiceException
from service import database_oracle

app = Blueprint('service_component', __name__, url_prefix='/service_component')
allow_component_type_list = ['database_oracle']


@app.route('/test', methods=['POST'])
def test():
    return 'test'


@app.route('/service_component', methods=['POST'])
def service_component():
    request_data = rest_form.check(['component_type', 'tag_id', 'params'])
    component_type = request_data['component_type']
    tag_id = request_data['tag_id']
    params = request_data['params']
    if component_type not in allow_component_type_list:
        raise MyServiceException('component_type not exists, please check again')
    return json.dumps(database_oracle.call_registration(tag_id, params))
