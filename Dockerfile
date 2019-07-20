FROM nginx:latest

MAINTAINER azure https://baiyue.one

ARG SOURCE=https://github.com/Baiyuetribe/ServerStatus-theme/archive/dev.zip

RUN apt update && apt-get install --no-install-recommends --no-install-suggests -y \
    gcc g++ make wget unzip \
    && wget --no-check-certificate ${SOURCE} && unzip dev.zip \
    && cp -rf /ServerStatus-theme-dev/web/* /usr/share/nginx/html/ \
    && rm -rf /ServerStatus-theme-dev/clients/* dev.zip \
    && cd /ServerStatus-theme-dev/server && make \
    && apt-get remove --purge --auto-remove -y gcc g++ make wget unzip && rm -rf /var/lib/apt/lists/*

EXPOSE 80 3561

RUN chmod +x /ServerStatus-theme-dev/entrypoint.sh

ENTRYPOINT ["/ServerStatus-theme-dev/entrypoint.sh"]