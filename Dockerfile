FROM nginx:latest

MAINTAINER azure https://baiyue.one

ARG SOURCE=https://github.com/91yun/ServerStatus

RUN apt update && apt-get install --no-install-recommends --no-install-suggests -y \
    gcc g++ make git \
    && git clone -b dev ${SOURCE} \
    && cp -rf /ServerStatus/web/* /usr/share/nginx/html/ \
    && rm -rf /ServerStatus/clients/* \
    && cd /ServerStatus/server && make \
    && apt-get remove --purge --auto-remove -y gcc g++ make git && rm -rf /var/lib/apt/lists/*

EXPOSE 80 3561

RUN chmod +x /ServerStatus/entrypoint.sh

ENTRYPOINT ["/ServerStatus/entrypoint.sh"]