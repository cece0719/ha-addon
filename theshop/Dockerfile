FROM python:3

ENV LANG C.UTF-8

#RUN apk add --no-cache python3
#RUN apk add --no-cache py3-pip

RUN python3 -m pip install pyserial
RUN python3 -m pip install paho-mqtt

COPY run.sh /
COPY run.py /
RUN chmod a+x /run.sh

WORKDIR /share

CMD [ "/run.sh" ]