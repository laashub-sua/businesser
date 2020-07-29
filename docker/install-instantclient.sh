apt-get update
apt-get -y install libaio-dev
sh -c "echo /opt/oracle/instantclient_19_6 > /etc/ld.so.conf.d/oracle-instantclient.conf"
ldconfig
mkdir -p /opt/oracle
wget https://download.oracle.com/otn_software/linux/instantclient/19800/instantclient-basic-linux.x64-19.8.0.0.0dbru.zip -O /opt/oracle/instantclient-basic-linux.x64-19.8.0.0.0dbru.zip
unzip /opt/oracle/instantclient-basic-linux.x64-19.8.0.0.0dbru.zip -d /opt/oracle
export LD_LIBRARY_PATH=/opt/oracle/instantclient_19_6:$LD_LIBRARY_PATH