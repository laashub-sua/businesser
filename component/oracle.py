"""
package the oracle operation
"""
import os
import platform

import cx_Oracle

from component import logging_ as logging
from component import path

operation_system_name = 'windows'
if platform.system() != "Windows":
    operation_system_name = 'linux'
cx_Oracle.init_oracle_client(
    lib_dir=os.path.join(path.find_third_party_path(), operation_system_name, 'instantclient_19_6'))


class Oracle(object):
    def __init__(self, ip, port, instance, username, password):

        tns = cx_Oracle.makedsn(ip, port, instance)
        self.connect = cx_Oracle.connect(username, password, tns)
        logging.info(tns)
        logging.info(self.connect.version)

    def __del__(self):
        self.connect.close()

    def select(self, sql, params=None):
        cur = self.connect.cursor()
        cur.execute(sql, params)
        execute_result = []
        # metadata
        metadata_column_list = []
        for column in cur.description:
            metadata_column_list.append(column[0])
        # data
        # row = cur.fetchone()
        rows = cur.fetchall()
        for row in rows:
            execute_result_item = {}
            for index in range(len(row)):
                execute_result_item[metadata_column_list[index].lower()] = row[index]
            execute_result.append(execute_result_item)
        return execute_result
