# ServerStatus中文版：   

* ServerStatus中文版是一个酷炫高逼格的云探针、云监控、服务器云监控、多服务器探针~，该云监控（云探针）是ServerStatus（ https://github.com/BotoX/ServerStatus ）项目的中文（优化）版。
* 在线演示：https://tz.cloudcpp.com  

这个版本是91yun在原来的基础进行了以下改动：
* 增加了探测被墙的状态
* 增加了服务器连接数的统计（总连接数/2）
* 下载速度改成了带宽显示（下载速度*8）
* 流量改成用vnstat统计当月流量（原来统计的是开机以来的总流量）
* 改用docker安装，集成了需要用户名密码登录的功能
* css适配了手机移动端的显示

# 目录介绍：

* clients  客户端文件
* server   服务端文件
* web      网站文件             

# 安装教程：     

【服务端配置】
          
一、服务器端依赖环境安装（docker和vnstat）           
```
yum install -y epel-release
yum -y install docker-io
service docker start
chkconfig docker on

yum install -y vnstat
service vnstat start
chkconfig vnstat on

```
二、创建docker镜像
```
#创建目录
mkdir /home/ServerStatus
#拉取默认配置文件
cd /home/ServerStatus
wget --no-check-certificate https://raw.githubusercontent.com/91yun/ServerStatus/master/server/config.json
#创建docker镜像
docker create --name=sss \
--restart=always \
-v /home/ServerStatus/config.json:/ServerStatus/server/config.json \
-p 3561:3561 \
-p 80:80 \
rongdede/serverstatus:server
```


三、修改服务器配置文件         
    vim /home/ServerStatus/config.json
修改config.json文件，注意username, password的值需要和客户端对应一致
password可以所有客户端都一样，但是username必须确保所有客户端都是唯一的                
```
{"servers":
	[
		{
			"username": "s01",
			"name": "Mainserver 1",
			"type": "Dedicated Server",
			"host": "GenericServerHost123",
			"location": "Austria",
			"password": "some-hard-to-guess-copy-paste-password"
		},
	]
}       
```

四、运行服务端：             
```
docker start sss
```

五、进阶应用：添加需要用户名和密码登录才能查看的功能
创建docker镜像的时候，增加两个参数 USERNAME和PASSWORD
```
docker create --name=sss \
--restart=always \
-v /home/ServerStatus/config.json:/ServerStatus/server/config.json \
-p 3561:3561 \
-p 80:80 \
-e "USERNAME=admin" \
-e "PASSWORD=baiyue.one" \
rongdede/serverstatus:server
```

【客户端配置】
```
yum -y install epel-release
yum -y install python-pip
yum clean all
yum -y install gcc
yum -y install python-devel
pip install psutil
mkdir -p /home/serverstatus
cd /home/serverstatus
wget https://github.com/91yun/ServerStatus-1/raw/master/clients/client-psutil.py
```
编辑客户端配置文件
    vim client-psutil.py
```
SERVER = "127.0.0.1" #改成呢你的服务器地址
PORT = 3561
USER = "USER" #改成唯一的客户端用户名，服务器根据这个字段判断是哪台服务器
PASSWORD = "USER_PASSWORD" #修改你的密码，和其他客户端可以是相同的
```
启动客户端
```
nohup python /home/serverstatus/client-psutil.py &> /dev/null &
```

# 相关开源项目，感谢： 

* ServerStatus：https://github.com/BotoX/ServerStatus
* mojeda: https://github.com/mojeda 
* mojeda's ServerStatus: https://github.com/mojeda/ServerStatus
* BlueVM's project: http://www.lowendtalk.com/discussion/comment/169690#Comment_169690
