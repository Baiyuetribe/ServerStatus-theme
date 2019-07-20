# -*- coding: utf-8 -*-
# Update by : https://github.com/tenyue/ServerStatus
# 依赖于psutil跨平台库：
# 支持Python版本：2.6 to 3.5 (users of Python 2.4 and 2.5 may use 2.1.3 version)
# 支持操作系统： Linux, Windows, OSX, Sun Solaris, FreeBSD, OpenBSD and NetBSD, both 32-bit and 64-bit architectures

SERVER = "127.0.0.1" #改成呢你的服务器地址
PORT = 2522
USER = "USER_NAME" #改成唯一的客户端用户名，服务器根据这个字段判断是哪台服务器
PASSWORD = "YoJOgLatMCYOqeq2h1UQ" #可自定义，前提是与前端一致

INTERVAL = 1 # 请勿修改
import socket
import time
import string
import math
import os
import json
import collections
import psutil
import commands

#========自定义的内容==========
#是否被墙
def ip_status():
	#14.215.177.39是百度的ip
	#123.125.115.110 也是百度的ip
	#117.136.190.162 10086的ip

	object_check = ['123.125.115.110', '14.215.177.39', '117.136.190.162']
	ip_check = 0
	for i in object_check:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(1)
		try:
			s.connect((i, 80))
			ip_check=1
			break
		except:
			continue
		s.close()
	if ip_check==1:
		return True
	else:
		return False
#连接数
def get_connections():
	cg="ss -s | awk '/estab/{a=gensub(/.*estab ([0-9]+),.*/,\"\\\\1\",1,$0);print a}'"
	(status, output) = commands.getstatusoutput(cg)
	return int(output)


def get_uptime():
	return int(time.time() - psutil.boot_time())

def get_memory():
	Mem = psutil.virtual_memory()
	try:
		MemUsed = Mem.total - (Mem.cached + Mem.free)
	except:
		MemUsed = Mem.total - Mem.free
	return int(Mem.total/1024.0), int(MemUsed/1024.0)

def get_swap():
	Mem = psutil.swap_memory()
	return int(Mem.total/1024.0), int(Mem.used/1024.0)

def get_hdd():
	valid_fs = [ "ext4", "ext3", "ext2", "reiserfs", "jfs", "btrfs", "fuseblk", "zfs", "simfs", "ntfs", "fat32", "exfat", "xfs" ]
	disks = dict()
	size = 0
	used = 0
	for disk in psutil.disk_partitions():
		if not disk.device in disks and disk.fstype.lower() in valid_fs:
			disks[disk.device] = disk.mountpoint
	for disk in disks.itervalues():
		usage = psutil.disk_usage(disk)
		size += usage.total
		used += usage.used
	return int(size/1024.0/1024.0), int(used/1024.0/1024.0)

def get_load():
	try:
		return os.getloadavg()[0]
	except:
		return -1.0

def get_cpu():
	return psutil.cpu_percent(interval=INTERVAL)

class Traffic:
	def __init__(self):
		self.rx = collections.deque(maxlen=10)
		self.tx = collections.deque(maxlen=10)
	def get(self):
		avgrx = 0; avgtx = 0
		for name, stats in psutil.net_io_counters(pernic=True).iteritems():
			if name == "lo" or name.find("tun") > -1:
				continue
			avgrx += stats.bytes_recv
			avgtx += stats.bytes_sent

		self.rx.append(avgrx)
		self.tx.append(avgtx)
		avgrx = 0; avgtx = 0

		l = len(self.rx)
		for x in range(l - 1):
			avgrx += self.rx[x+1] - self.rx[x]
			avgtx += self.tx[x+1] - self.tx[x]

		avgrx = int(avgrx / l / INTERVAL)
		avgtx = int(avgtx / l / INTERVAL)

		return avgrx, avgtx

def liuliang():
	NET_IN = 0
	NET_OUT = 0
	vnstat=os.popen('vnstat --dumpdb').readlines()
	for line in vnstat:
		if line[0:4] == "m;0;":
			mdata=line.split(";")
			NET_IN=int(mdata[3])*1024*1024
			NET_OUT=int(mdata[4])*1024*1024
			break
	return NET_IN, NET_OUT

def get_network(ip_version):
	if(ip_version == 4):
		HOST = "ipv4.google.com"
	elif(ip_version == 6):
		HOST = "ipv6.google.com"
	try:
		s = socket.create_connection((HOST, 80), 2)
		return True
	except:
		pass
	return False

if __name__ == '__main__':
	socket.setdefaulttimeout(30)
	while 1:
		try:
			print("Connecting...")
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((SERVER, PORT))
			data = s.recv(1024)
			if data.find("Authentication required") > -1:
				s.send(USER + ':' + PASSWORD + '\n')
				data = s.recv(1024)
				if data.find("Authentication successful") < 0:
					print(data)
					raise socket.error
			else:
				print(data)
				raise socket.error

			print(data)
			data = s.recv(1024)
			print(data)

			timer = 0
			check_ip = 0
			if data.find("IPv4") > -1:
				check_ip = 6
			elif data.find("IPv6") > -1:
				check_ip = 4
			else:
				print(data)
				raise socket.error

			traffic = Traffic()
			traffic.get()
			while 1:
				CPU = get_cpu()
				NetRx, NetTx = traffic.get()
				NET_IN, NET_OUT = liuliang()
				Uptime = get_uptime()
				Load = get_load()
				MemoryTotal, MemoryUsed = get_memory()
				SwapTotal, SwapUsed = get_swap()
				HDDTotal, HDDUsed = get_hdd()
				#=====自己加的
				IPStatus=ip_status()
				Connections=get_connections()

				array = {}
				if not timer:
					array['online' + str(check_ip)] = get_network(check_ip)
					timer = 10
				else:
					timer -= 1*INTERVAL

				array['uptime'] = Uptime
				array['load'] = Load
				array['memory_total'] = MemoryTotal
				array['memory_used'] = MemoryUsed
				array['swap_total'] = SwapTotal
				array['swap_used'] = SwapUsed
				array['hdd_total'] = HDDTotal
				array['hdd_used'] = HDDUsed
				array['cpu'] = CPU
				array['network_rx'] = NetRx
				array['network_tx'] = NetTx
				array['network_in'] = NET_IN
				array['network_out'] = NET_OUT
				array['ip_status'] = IPStatus
				array['connections'] = Connections

				s.send("update " + json.dumps(array) + "\n")
		except KeyboardInterrupt:
			raise
		except socket.error:
			print("Disconnected...")
			# keep on trying after a disconnect
			s.close()
			time.sleep(3)
		except Exception as e:
			print("Caught Exception:", e)
			s.close()
			time.sleep(3)
