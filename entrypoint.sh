#!/bin/sh

if [ $USERNAME ]
then
	if [ ! $PASSWORD ]
	then
		PASSWORD="baiyue.one"
	fi
	mv -f /ServerStatus-theme-dev/default.conf /etc/nginx/conf.d/default.conf
	printf "${USERNAME}:$(openssl passwd -crypt ${PASSWORD})\n" >> /ServerStatus-theme-dev/htpasswd
	chmod 777 /ServerStatus-theme-dev/htpasswd
fi

nohup /etc/init.d/nginx start && /ServerStatus-theme-dev/server/sergate --config=/ServerStatus-theme-dev/server/config.json --port=2522 --web-dir=/usr/share/nginx/html


/etc/init.d/nginx start 
nohup /ServerStatus-theme-dev/server/sergate --config=/ServerStatus-theme-dev/server/config.json --port=2522 --web-dir=/usr/share/nginx/html



