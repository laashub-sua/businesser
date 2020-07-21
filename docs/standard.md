-------------------------- 开发时:

四层数据:



组件类型: database_oracle

​	标识id: 报账系统_报账单_信息

​		执行数据: xxx.sql: :<变量名>



-------------------------- 调用时:

通过rest调用, 传递参数为: 



‘component_type’: 组件类型, 例如: database_oracle

'tag_id': 标识id, 例如: analysis_report

'params': 参数, 例如: {"accounting_code": "Z01110010000000000", "duration": "202006"}



-------------------------- 集成时-修改配置文件:

data/service_component/database_oracle/database_oracle.yml



analysis_report: # 标识id

​	database_config_file_path: analysis_report/datasource.yml # 数据库配置文件(默认值为: datasource.yml, 保留一层目录是为了重用)

​	sql_file_path: analysis_report/sql.sql # sql文件位置(默认值为: sql.sql, 保留一层目录是为了重用)

​	



-------------------------- 集成时-编写sql文件:

data/service_component/database_oracle/data/analysis_report/sql.sql



select * from table1



-------------------------- 集成时-修改数据库连接配置文件:

data/service_component/database_oracle/data/analysis_report/datasource.yml



ip: 1.1.1.1

port: 1521

instance: test

username: test

password: test



-------------------------- 部署时:

挂载目录到宿主机(-v)

data/service_component/database_oracle/database_oracle.yml

data/service_component/database_oracle/data

