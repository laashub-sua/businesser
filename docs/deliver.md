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
mv -f /etc/yum.repos.d/CentOS-Base.repo.bak /etc/yum.repos.d/CentOS-Base.repo

mv -f /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.bak
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
yum install -y epel-release
wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
yum clean all
yum makecache


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
mkdir -p /data/tristan/laashub-sua/businesser/configs && chmod 777 /data/tristan/laashub-sua/businesser/configs

mkdir -p /data/tristan/laashub-sua/businesser/data/service_component/database_oracle/data && chmod 777 /data/tristan/laashub-sua/businesser/data/service_component/database_oracle/data

docker run --name businesser laashubsua/businesser
docker cp businesser:/usr/src/app/configs /data/tristan/laashub-sua/businesser/configs
docker cp businesser:/usr/src/app/data/service_component/database_oracle /data/tristan/laashub-sua/businesser/data/service_component/database_oracle
```

实际使用

```
docker stop businesser
docker rm businesser
docker rmi laashubsua/businesser
docker run -d --restart=always --name businesser -p 5000:5000 \
  -v /data/tristan/laashub-sua/businesser/configs/application.yml:/usr/src/app/configs/application.yml \
  -v /data/tristan/laashub-sua/businesser/data/service_component/database_oracle/registration.yaml:/usr/src/app/data/service_component/database_oracle/registration.yaml \
  -v /data/tristan/laashub-sua/businesser/data/service_component/database_oracle/data/:/usr/src/app/data/service_component/database_oracle/data/ \
  laashubsua/businesser
```



```
docker stop businesser
docker rm businesser
docker run -it --restart=always --name businesser -p 5000:5000 \
  -v /data/tristan/laashub-sua/businesser/configs/application.yml:/usr/src/app/configs/application.yml \
  -v /data/tristan/laashub-sua/businesser/data/service_component/database_oracle/registration.yaml:/usr/src/app/data/service_component/database_oracle/registration.yaml \
  -v /data/tristan/laashub-sua/businesser/data/service_component/database_oracle/data/:/usr/src/app/data/service_component/database_oracle/data/ \
  laashubsua/businesser bash
```



```
docker run -it laashubsua/businesser
docker run -it --restart=always --name businesser -p 5000:5000 \
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

