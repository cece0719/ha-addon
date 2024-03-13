#ARG BUILD_FROM="alpine:latest"
#ARG BUILD_FROM
#FROM $BUILD_FROM
FROM node:latest

ENV LANG C.UTF-8

# Copy data for add-on
COPY run.sh /
COPY js /js
#
## Install requirements for add-on
RUN npm init -f && \
    npm install mqtt && \
    npm install serialport --build-from-source=serialport

WORKDIR /share

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]