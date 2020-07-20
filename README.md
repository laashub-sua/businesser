[原文地址](https://github.com/laashub-sua/laas-sua/blob/master/docs/businesser.md)

businesser

业务器

以业务为核心, 以业务方式去做自动化, 简单了当

例如:

数据库组件

编写业务场景的数据查询SQL获取数据, 在场景、系统、模块、功能四个层次上去注册标识, SUA通过标识去调用SQL

分为四个数据: 1、标识字符串 2、业务类型, 例如: SQL 3、SQL内容 4、参数

数据保存在businesser本地

通过username-password登录认证鉴权

校验传入参数

预编译SQL

执行SQL并传递参数

得到SQL执行结果

响应json序列化的SQL执行结果

提供web界面添加数据库连接信息/修改项目配置文件(datasource.yml)

使用iptables 配置businesser所在服务器对SUA调用方: runner 的ip进行放行

使用docker方式部署, 基于system开启自启机制保证docker进程运行, 基于docker自启机制保证 docker容器运行

如果需要设置多节点实现不宕机、热升级, 可选:

 使用nginx负载多个docker容器

 本地域名指向多个主机上的docker容器