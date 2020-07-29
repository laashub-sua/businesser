FROM python:3.7
# oracle client
RUN docker/install-instantclient.sh
# app
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
EXPOSE 5000
CMD [ "python", "./setup.pyc" ]