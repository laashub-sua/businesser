import os

from component import configer
from component import logging_ as logging
from component import path
from component.oracle import Oracle
from exception import MyServiceException
from . import database_oracle

local_data_registration = {}
local_data_data = {}

database_oracle_dir_path = os.path.join(path.find_tag_path(path_tag='data'), 'service_component/database_oracle')
datasource_file_path_str = 'datasource_file_path'
datasource_file_path_default = 'datasource.yml'
sql_file_path_str = 'sql_file_path'
sql_file_path_default = 'sql.sql'


def load_local_data(tag_id):
    # config file
    if tag_id not in database_oracle.local_data_registration:
        database_oracle.local_data_registration = configer.load(
            os.path.join(database_oracle_dir_path, 'registration.yaml'))
    if tag_id not in database_oracle.local_data_registration:
        raise MyServiceException('the target tag id(%s) is not exists in service component: database_oracle' % tag_id)
    cur_config = database_oracle.local_data_registration[tag_id]
    if cur_config:
        if datasource_file_path_str in cur_config:
            datasource_file_path = cur_config[datasource_file_path_str]
        if sql_file_path_str in cur_config:
            sql_file_path = cur_config[sql_file_path_str]
    else:
        datasource_file_path = datasource_file_path_default
        sql_file_path = sql_file_path_default
    if '/' not in datasource_file_path:
        datasource_file_path = os.path.join(tag_id, datasource_file_path)
    if '/' not in sql_file_path:
        sql_file_path = os.path.join(tag_id, sql_file_path)
    cur_data_dir_path = os.path.join(database_oracle_dir_path, 'data')
    datasource_file_path = os.path.join(cur_data_dir_path, datasource_file_path)
    sql_file_path = os.path.join(cur_data_dir_path, sql_file_path)
    logging.info('datasource_file_path: ' + datasource_file_path)
    logging.info('sql_file_path: ' + sql_file_path)
    if not os.path.exists(datasource_file_path):
        raise MyServiceException('datasource is not exists')
    if not os.path.exists(sql_file_path):
        raise MyServiceException('sql is not exists')
    # data
    datasource_content = configer.load(datasource_file_path)
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    return datasource_content, sql_content


def check_datasource_content(datasource_content, check_list):
    if not datasource_content:
        raise MyServiceException('datasource_content is None')
    for item in check_list:
        if item not in datasource_content:
            raise MyServiceException('%s not in datasource.yml' % item)


def call_registration(tag_id, params):
    datasource_content, sql_content = load_local_data(tag_id)
    check_datasource_content(datasource_content, ['ip', 'port', 'instance', 'username', 'password'])
    if not sql_content or sql_content.strip() == '':
        raise MyServiceException('sql_content is None or space')

    ip = datasource_content['ip']
    port = datasource_content['port']
    instance = datasource_content['instance']
    username = datasource_content['username']
    password = datasource_content['password']

    oracle = Oracle(ip=ip, port=port, instance=instance, username=username, password=password)
    return oracle.select(sql_content, params=params)
