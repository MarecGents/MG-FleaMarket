import datetime
import json
import os
from os import path

import requests

ERROR = "error"
NOT_FOUND = "not_found"


class MGDate:
	@staticmethod
	def get_Date():
		date = datetime.datetime.now()
		return [date.year, date.month, date.day]
	
	pass


class FileControl:
	@staticmethod
	def getJsonFileByAbsolutePath(absolute_path):
		with open(absolute_path, 'r', encoding='utf-8') as f_r:
			file = json.load(f_r)
			return file
		pass
		
	
	@staticmethod
	def saveJsonFileByAbsolutePath(absolute_path, content):
		with open(absolute_path, 'w', encoding='utf-8') as f_w:
			json.dump(content, f_w, ensure_ascii=False, indent=4)
		return True
	
	pass


class HttpControl:
	@staticmethod
	def getBaseInfoFromTarkovAPI(path, headers, body):
		resp = requests.post(path, headers=headers, json=body)
		resp.encoding = 'utf-8'
		content = resp.json()
		resp.close()
		return content
	
	pass


class PathControl:
	@staticmethod
	def getNowFilePath(_file_):
		return path.realpath(_file_)
	
	@staticmethod
	def getNowFolderPath(_file_):
		if path.isfile(_file_):
			return path.dirname(PathControl.getNowFilePath(_file_))
		else:
			return _file_
	@staticmethod
	def getPathByFilePathOrFolderPath(_file_):
		if path.isfile(_file_):
			return PathControl.getNowFolderPath(_file_)
		elif path.isdir(_file_):
			return _file_
		else:
			return ERROR
	
	@staticmethod
	def getParentFolderPath(_file_):
		return path.dirname(PathControl.getPathByFilePathOrFolderPath(_file_))
	
	@staticmethod
	def getParentsFolderPath(_file_, times):
		temp_path = PathControl.getPathByFilePathOrFolderPath(_file_)
		if times == 0:
			return temp_path
		elif times >= 1:
			for i in range(times):
				temp_path = PathControl.getParentFolderPath(temp_path)
				pass
			return temp_path
		else:
			return ERROR
		pass
	
	@staticmethod
	def getSubFolderPath(_file_, folder_name):
		now_folder_path = PathControl.getPathByFilePathOrFolderPath(_file_)
		if (now_folder_path is not None) and (folder_name in os.listdir(now_folder_path)):
			return path.join(now_folder_path, folder_name)
		else:
			return ERROR
		pass
	
	# sub_or_parent
	@staticmethod
	def locateGivenFolderNamePathNearby(_file_, folder_name):
		"""
		:param _file_: the absolut path of code running file
		:param folder_name: the absolut path of folder you want to locate and get
		:param sub_or_parent: is aim to present where to find the folder now is subDir or parentDir relative _file_ path when the value is larger than 0 presenting to find in n-th level parentDir, smaller than 0 is so on in subDir.
		:return: is the absolut path of folder you want to find by name
		"""
		
		now_path = PathControl.getPathByFilePathOrFolderPath(_file_)
		if folder_name in os.listdir(now_path):
			# already find aiming folder
			return path.join(now_path, folder_name)
		# can not find in above folder space
		# turn to find in subDirs
		aim_path = None
		for it in os.listdir(now_path):
			temp_path = PathControl.getSubFolderPath(now_path, it)
			if (temp_path is ERROR) or (not os.path.isdir(temp_path)):
				continue
				pass
			aim_path = PathControl.locateGivenFolderNamePathNearby(temp_path, folder_name)
			if path.isdir(aim_path):
				return aim_path
			pass
		if aim_path is NOT_FOUND or aim_path is None:
			return NOT_FOUND
		pass
	
	@staticmethod
	def getFolderNameByPath(_path_):
		if os.path.isdir(_path_):
			return path.split('/')[-1]
		else:
			return ERROR
		pass
	
	pass
