FROM nginx

MAINTAINER Baiyuetribe

RUN apt-get update
RUN apt-get -y install gcc g++ make git
RUN git clone https://github.com/Baiyuetribe/ServerStatus
RUN cp -rf /ServerStatus/web/* /usr/share/nginx/html/


WORKDIR /ServerStatus/server

RUN make
RUN pwd && ls -a

EXPOSE 80 35601

CMD nohup sh -c '/etc/init.d/nginx start && /ServerStatus/server/sergate --config=/ServerStatus/server/config.json --web-dir=/usr/share/nginx/html'
