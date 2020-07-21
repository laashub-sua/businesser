[原文地址](https://github.com/laashub-sua/laas-sua/blob/master/docs/businesser.md)

[更多更详细文档: 点击docs](docs)

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

# standard

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



# featrue



动态加载指定目录中所有配置文件到项目中

动态加载指定目录(rest)中所有app到项目蓝图中

自动配置日志

使用本地文件方式代替数据库

懒加载database_oracle注册文件

加载datasource和sql文件

使用token进行认证

rest风格接口

自带Dockerfile, 使用官方CI, 直接拉取镜像使用即可

自带部署shell

使用docker方式可以提高部署的效率和稳定性



使用文件隔离, 提高安全性

使用数据注册风格, 从某个角度上验证了distribution的作用, 为后续distribution打下铺垫

# deliver

镜像仓库地址:

https://hub.docker.com/r/laashubsua/businesser

Dockerfile:

```
# 后端
FROM python:3.7
WORKDIR /usr/src/app
RUN rm -rf *
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
RUN python3 -m compileall -b .
RUN find . -name "*.py" |xargs rm -rf
# 声明
MAINTAINER tristan "https://github.com/laashub-sua/businesser"
VOLUME /usr/src/app/configs/application.yml
VOLUME /usr/src/app/data/service_component/database_oracle/registration.yaml
VOLUME /usr/src/app/data/service_component/database_oracle/data
EXPOSE 5000
CMD [ "python", "./setup.pyc" ]
```

挂载目录:

```
/usr/src/app/configs/application.yml
/usr/src/app/data/service_component/database_oracle/registration.yaml
/usr/src/app/data/service_component/database_oracle/data
```

指令:

安装docker

```
echo "install docker"
curl -sSL get.docker.com | sh
systemctl start docker.service
systemctl enable docker.service

echo "docker调优"
echo "关闭selinux"
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config

echo "修改时区为上海"
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

echo "修改系统语言环境"
echo 'LANG="en_US.UTF-8"' >> /etc/profile;source /etc/profile

echo "同步时间"
yum install -y ntp
ntpdate pool.ntp.org
systemctl enable ntpd

echo "kernel性能调优:"
echo "1、修复可能出现的网络问题"
echo "2、修改最大进程数"
sudo cat >> /etc/sysctl.conf<<EOF
net.ipv4.ip_forward=1
net.bridge.bridge-nf-call-iptables=1
net.ipv4.neigh.default.gc_thresh1=4096
net.ipv4.neigh.default.gc_thresh2=6144
net.ipv4.neigh.default.gc_thresh3=8192
kernel.pid_max=1000000
EOF
systemctl restart network
sysctl -p

echo "关闭防火墙"
firewall-cmd --state
systemctl stop firewalld.service
systemctl disable firewalld.service

echo "设置docker加速器"
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
   "registry-mirrors": [
       "https://mirror.ccs.tencentyun.com"
  ]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```

启动

准备动作

```
mkdir -p /data/tristan/laashub-sua/businesser && chmod 777 /data/tristan/laashub-sua/businesser
docker run --name businesser laashub-sua/businesser
docker cp businesser:/usr/src/app/configs/application.yml /data/tristan/laashub-sua/businesser/configs/application.yml
docker cp businesser:/usr/src/app/data/service_component/database_oracle/registration.yaml /data/tristan/laashub-sua/businesser/data/service_component/database_oracle/registration.yaml

mkdir -p /data/tristan/laashub-sua/businesser/data/service_component/database_oracle/data && chmod 777 /data/tristan/laashub-sua/businesser/data/service_component/database_oracle/data
```

实际使用

```
docker stop businesser
docker rm businesser
docker rmi laashubsua/businesser
docker run -d --restart=always --name businesser -p 5000:5000 \
  -v /data/tristan/laashub-sua/businesser/configs/application.yml:/usr/src/app/configs/application.yml \
  -v /data/tristan/laashub-sua/businesser/data/service_component/database_oracle/registration.yaml:/usr/src/app/data/service_component/database_oracle/registration.yaml \
  -v /data/tristan/laashub-sua/businesser/data/service_component/database_oracle/data:/usr/src/app/data/tristan/laashub-sua/businesser/data/service_component/database_oracle/data \
  laashubsua/businesser
```

查看日志

```
docker logs -f --tail 100 businesser
docker exec -it businesser bash
```

防火墙设置

```
# 启动iptables
yum install -y iptables-services
systemctl start  iptables
systemctl enable iptables

# 禁止其他ip访问本地的该端口
iptables -I INPUT -p tcp --dport 5000 -j DROP

# 放行指定ip能够访问本地的该端口
iptables -I INPUT -s 10.10.233.26 -ptcp --dport 5000 -j ACCEPT
```



# dev

python 版本: 3.7

安装依赖库:

pip install -r requirements.txt



导出本地依赖文件清单到文件:

pip freeze > requirements.txt



设置以解决超过100M的单文件提交失败

```
git lfs install
git lfs track "*.dll"
git add .gitattributes
git add test.dll
git commit -m "commit"
git push origin master
```

