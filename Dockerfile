FROM ubuntu:18.04

WORKDIR /hicn

# Use bash shell
SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get install python3.6 -y
RUN apt-get install python3 -y && apt install python-pip -y && apt install python3-pip -y
RUN pip3 install pyyaml && apt install python3-pyparsing -y && pip3 install janus &&  apt install python3-lockfile -y && apt install python3-daemon -y && pip3 install autobahn
RUN pip3 install requests && pip3 install avro-python3 && pip3 install kafka && pip install influxdb && pip3 install aiomysql && pip3 install aiopg && apt install apache2 -y && pip install progressbar

RUN mkdir cntrl

COPY config.xml odl.py tnode.xml cntrl/

WORKDIR /hicn
