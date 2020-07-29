"""
package the oracle operation
"""
import platform

import cx_Oracle

from component import logging_ as logging

if platform.system() == "Windows":
    cx_Oracle.init_oracle_client(
        lib_dir=r'D:\program_files\oracle_client\windows\instantclient_19_6')
else:
    cx_Oracle.init_oracle_client()


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


