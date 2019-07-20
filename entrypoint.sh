#!/bin/bash

if [ $USERNAME ]
then
	if [ ! $PASSWORD ]
	then
		PASSWORD="baiyue.one"
	fi
	mv -f /ServerStatus/default.conf /etc/nginx/conf.d/default.conf
	printf "${USERNAME}:$(openssl passwd -crypt ${PASSWORD})\n" >> /ServerStatus/htpasswd
	chmod 777 /ServerStatus/htpasswd
fi

nohup /etc/init.d/nginx start && /ServerStatus/server/sergate --config=/ServerStatus/server/config.json --port=2522 --web-dir=/usr/share/nginx/html


/etc/init.d/nginx start 
nohup /ServerStatus/server/sergate --config=/ServerStatus/server/config.json --port=2522 --web-dir=/usr/share/nginx/html



