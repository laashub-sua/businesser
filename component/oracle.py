"""
package the oracle operation
"""
import cx_Oracle

db = cx_Oracle.connect('admin/123456@127.0.0.1:1521/orcl')
print(db.version)
db.close()


