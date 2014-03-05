# -*- coding: utf-8 -*-
#!/usr/bin/python  
import sys
import os
import ftplib
import socket

CONST_HOST = "10.214.9.220"  # your ftp host
CONST_USERNAME = "root"      # your login name
CONST_PWD = "raspberry"      # your password
CONST_BUFFER_SIZE = 8192     # give a buffer size
CONST_WORKPWD = "/home/whatever/Dropbox/whateverblog"  # from where
FTP_WORKPWD = "/var/www/whateverblog/"     # to where

COLOR_NONE = "\033[m"  
COLOR_GREEN = "\033[01;32m"  
COLOR_RED = "\033[01;31m"  
COLOR_YELLOW = "\033[01;33m"  

#connect ftp
def connect():
	try:
		ftp = ftplib.FTP(CONST_HOST)
		ftp.login(CONST_USERNAME, CONST_PWD)
		return ftp
	except socket.error,socket.gaierror:  
		print("FTP is unavailable, please check the host,username and password!")  
	sys.exit(0)

#disconnect ftp
def disconnect(ftp):  
	ftp.quit()

# upload file
def upload(ftp, filepath):  
	f = open(filepath, "rb")  
	file_name = os.path.split(filepath)[-1]  
	try:  
		ftp.storbinary('STOR %s'%file_name, f, CONST_BUFFER_SIZE)  
	except ftplib.error_perm:  
		return False  
	return True  

# dele direction
def rmftpdir(ftp, newdir):
	for lists in ftp.nlst(newdir):
		# print lists
		try:
			ftp.cwd(os.path.join(newdir,lists))
			rmftpdir(ftp, os.path.join(ftp,os.path.join(newdir,lists)))
		except ftplib.error_perm:
			ftp.delete(os.path.join(newdir,lists))
	ftp.rmd(newdir)

# bianli and upload
def bianli(ftp, rootDir, ftpolddir):
	for lists in os.listdir(rootDir): 
		path = os.path.join(rootDir, lists)
		if os.path.isdir(path): 
			try:
				ftp.mkd(os.path.join(ftpolddir,lists)) # if can't make the direction, mean it is already exist
			except ftplib.error_perm:
				rmftpdir(ftp, os.path.join(ftp,ftpolddir,lists)) 
				ftp.mkd(os.path.join(ftpolddir,lists))
				print(("MAKEDIR: %s "+COLOR_GREEN+"SUCCESS"+COLOR_NONE)%lists)
			bianli(ftp, path, os.path.join(ftpolddir,lists))
		else:
			ftp.cwd(ftpolddir) #+ os.path.basename(path))
			upload(ftp, path) 
			print(("UPLOAD: %s "+COLOR_GREEN+"SUCCESS"+COLOR_NONE)%path)

def main():
	ftp = connect()

	os.chdir(CONST_WORKPWD)
	new_dir = ''
	bianli(ftp, CONST_WORKPWD, FTP_WORKPWD)

	# ftp.cwd(FTP_WORKPWD)
	# list = ftp.nlst()       # 获得目录列表
	# for name in list:
	# print(name)             # 打印文件名字
	
	disconnect(ftp)

if __name__ == "__main__":  
	main()  
