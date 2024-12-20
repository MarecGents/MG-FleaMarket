import datetime
import json
import os
from os import path
import subprocess
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
	def locateGivenFolderNamePathNearby(_file_, folder_name, keys=None):
		"""
		:param keys:
		:param _file_: the absolut path of code running file
		:param folder_name: the absolut path of folder you want to locate and get
		:param sub_or_parent: is aim to present where to find the folder now is subDir or parentDir relative _file_ path when the value is larger than 0 presenting to find in n-th level parentDir, smaller than 0 is so on in subDir.
		:return: is the absolut path of folder you want to find by name
		"""
		if keys is None:
			keys = None
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
			aim_path = PathControl.locateGivenFolderNamePathNearby(temp_path, folder_name, keys)
			is_compare = 0
			if keys and type(keys) == list:
				for key in keys:
					if key not in aim_path:
						is_compare = -1
					pass
				pass
			if is_compare == -1:
				continue
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
	
	@staticmethod
	def combineFolderPathWithRelativePath(_path_,relative_path):
		return path.join(_path_, relative_path)
	
	pass

class GitControl:
	
	@staticmethod
	def debugInfo(method,value):
		print(f"Debug Info --> {method}:", value.returncode, value.stdout.decode(), value.stderr.decode())
		pass
	
	@staticmethod
	def subRun(args, PWSH_PATH):
		return subprocess.run(args, cwd=PWSH_PATH, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
		pass
	
	@staticmethod
	def gitPull(PWSH_PATH):
		git_ins = subprocess.run(['git', 'pull'], cwd=PWSH_PATH, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
		GitControl.debugInfo("GIT PULL", git_ins)
		pass
	
	@staticmethod
	def gitAdd(PWSH_PATH):
		git_ins = subprocess.run(['git', 'add', '-A'], cwd=PWSH_PATH, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
		GitControl.debugInfo("GIT ADD", git_ins)
		pass
	
	@staticmethod
	def gitCommit(PWSH_PATH,message):
		git_ins = subprocess.run(['git', 'commit', '-m', message], cwd=PWSH_PATH, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
		GitControl.debugInfo("GIT COMMIT", git_ins)
		pass
	
	# @staticmethod
	# def gitCommitAdd(PWSH_PATH,message):
	# 	git_ins = subprocess.run(['git', 'commit', '-a', '-m', message], cwd=PWSH_PATH, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	# 	GitControl.debugInfo("GIT COMMIT WITH ADD", git_ins)
	# 	pass
	
	@staticmethod
	def gitPush(PWSH_PATH):
		git_ins = subprocess.run(['git', 'push'], cwd=PWSH_PATH, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
		GitControl.debugInfo("GIT PUSH", git_ins)
		pass
	
	@staticmethod
	def gitRefresh(PWSH_PATH,message):
		GitControl.gitAdd(PWSH_PATH)
		GitControl.gitCommit(PWSH_PATH,message)
		GitControl.gitPush(PWSH_PATH)
		pass
	
	
	pass
