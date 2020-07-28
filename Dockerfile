# oracle client
FROM oraclelinux:7-slim as builder
ARG release=19
ARG update=5
RUN yum -y install oracle-release-el7
RUN yum-config-manager --enable ol7_oracle_instantclient
RUN yum -y install oracle-instantclient${release}.${update}-basiclite
RUN rm -rf /usr/lib/oracle/${release}.${update}/client64/bin
WORKDIR /usr/lib/oracle/${release}.${update}/client64/lib/
RUN rm -rf *jdbc* *occi* *mysql* *jar
# project
FROM python:3.7
WORKDIR /usr/src/app
RUN rm -rf *
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
RUN python3 -m compileall -b .
RUN find . -name "*.py" |xargs rm -rf
MAINTAINER tristan "https://github.com/laashub-sua/businesser"
#VOLUME /usr/src/app/configs/application.yml
#VOLUME /usr/src/app/data/service_component/database_oracle/registration.yaml
#VOLUME /usr/src/app/data/service_component/database_oracle/data
# Copy the Instant Client libraries, licenses and config file from the previous image
COPY --from=builder /usr/lib/oracle /usr/lib/oracle
COPY --from=builder /usr/share/oracle /usr/share/oracle
COPY --from=builder /etc/ld.so.conf.d/oracle-instantclient.conf /etc/ld.so.conf.d/oracle-instantclient.conf
RUN apt-get update && apt-get -y upgrade && apt-get -y dist-upgrade && apt-get install -y libaio1 && \
    apt-get -y autoremove && apt-get -y clean && \
    ldconfig
EXPOSE 5000
CMD [ "python", "./setup.pyc" ]