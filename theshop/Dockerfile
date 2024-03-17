FROM python:3

ENV LANG C.UTF-8

#RUN apk add --no-cache python3
#RUN apk add --no-cache py3-pip

RUN python3 -m pip install pyserial
RUN python3 -m pip install 'paho-mqtt<2.0.0'

COPY run.sh /
COPY py /py
RUN chmod a+x /run.sh

WORKDIR /share

EXPOSE 8001

CMD [ "/run.sh" ]