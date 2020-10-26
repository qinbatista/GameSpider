import requests
import threading
import os, chardet, json
from random import choice, randint
import xlrd
import re
# from PIL import ImageGrab
import time
# from selenium import webdriver
from function import settings

dict_Web = {}
GameList = []
SABCD = ["S", "A", "B", "C", "D", "TBD"]


def GetEncoding(path):
	with open(path, 'rb') as f:
		encoding = chardet.detect(f.read())['encoding']
		return "utf-8" if encoding is None else encoding


def PythonLocation():
	return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class MyThread(threading.Thread):
	def run(self):
		try:
			try:
				response = requests.get(url=self._args[1], headers={'User-Agent': choice(settings.AGENTS)}, timeout=5)
			except:
				response = requests.get(url=self._args[1], headers={'User-Agent': choice(settings.AGENTS)}, timeout=5)
			path = settings.e2wGamePath + "/AppMonitor/" + settings.mkPath + "/Web/"
			for game in GameList:
				if (game + "_") in self._args[0]:
					path = path + game + "/"
					break
			with open(path + self._args[0] + ".html", 'w', encoding='utf-8') as out:
				out.write(re.search('[\s\S]*', response.text).group())
		except:
			print("access", self._args[1], "timeout")


def ReadJson(JsonLocation):
	readed = json.load(open(JsonLocation, 'r', encoding=GetEncoding(JsonLocation)))
	for key in readed.keys():
		if key not in SABCD:
			s = key.replace(':', '：').replace(' ', '_').replace('__', '_')
			if s[0] == '_':
				s = s[1:]
			GameList.append(s)
		for n in range(0, len(readed[key]), 2):
			if readed[key][n + 1] != '' and key not in SABCD and 'post' not in readed[key][n + 1]:
				s = key.replace(':', '：').replace(' ', '_').replace('__', '_') + '_' + readed[key][n]
				if s[0] == '_':
					s = s[1:]
				dict_Web.update({s: readed[key][n + 1].replace(' ', '')})


def ReadExcel():  # 暂时没有用
	sheet = xlrd.open_workbook(PythonLocation() + '/GamePublishList.xls').sheet_by_index(1)
	for row in range(sheet.nrows):
		if sheet.cell_value(row, 0) != 'S' and sheet.cell_value(row, 0) != 'A' and sheet.cell_value(row, 0) != 'B' and sheet.cell_value(
				row, 0) != 'C' and sheet.cell_value(row, 0) != 'D' and sheet.cell_value(row, 0) != 'TBD' and sheet.cell_value(
				row, 2) != '':
			if 'App' not in sheet.cell_value(row, 1):
				s = (sheet.cell_value(row, 0) + '_' + sheet.cell_value(row, 1)).replace('：', '_').replace(' ', '_').replace('__', '_')
				if s[0] == '_':
					s = s[1:]
				dict_Web.update({s: sheet.cell_value(row, 2).replace(' ', '')})
	print(dict_Web)


def SavePageWeb():
	path = settings.e2wGamePath + "/AppMonitor/" + settings.mkPath + "/Web"
	if not os.path.exists(path):
		os.mkdir(path)
	for game in GameList:
		if not os.path.exists(path + "/" + game):
			os.mkdir(path + "/" + game)
	threads = []
	for key in dict_Web.keys():
		threads.append(MyThread(args=(key, dict_Web.get(key))))
	nthreads = []
	for t in threads:
		t.start()
		nthreads.append(t)
		if len(nthreads) > 1000:
			for n in nthreads:
				n.join()
			nthreads = []
	for n in nthreads:
		n.join()


"""
def SaveWebImage():
	timeout_dict = {}
	path = settings.e2wGamePath + "/AppMonitor/" + settings.mkPath + "/WebImage"
	if not os.path.exists(path):
		os.mkdir(path)
	for game in GameList:
		if not os.path.exists(path + "/" + game):
			os.mkdir(path + "/" + game)
	driver = webdriver.Chrome()
	driver.implicitly_wait(10)
	driver.maximize_window()
	for key in dict_Web.keys():
		try:
			print('name:', key, '.png   url:', dict_Web.get(key), sep="")
			print("Time:", time.strftime("%H:%M:%S", time.localtime(time.time())), sep="")
			driver.get(dict_Web.get(key).replace(' ', ''))
			path = settings.e2wGamePath + "/AppMonitor/" + settings.mkPath + "/WebImage"
			for game in GameList:
				if (game + "_") in key:
					path = path + "/" + game + "/"
					break
			dict_size = driver.get_window_size()
			time.sleep(3)
			image = ImageGrab.grab((100, 110, dict_size.get('width') - 200, dict_size.get('height') - 20))
			image.save(path + key + ".png")
		except:
			timeout_dict.update({key: dict_Web.get(key).replace(' ', '')})
	for key in timeout_dict.keys():
		print('name:', key, '.png   url:', timeout_dict.get(key), sep="")
		print("Time:", time.strftime("%H:%M:%S", time.localtime(time.time())), sep="")
		driver.get(timeout_dict.get(key))
		path = settings.e2wGamePath + "/AppMonitor/" + settings.mkPath + "/WebImage"
		for game in GameList:
			if (game + "_") in key:
				path = path + "/" + game + "/"
				break
		dict_size = driver.get_window_size()
		time.sleep(3)
		image = ImageGrab.grab((100, 110, dict_size.get('width') - 200, dict_size.get('height') - 20))
		image.save(path + key + ".png")
	driver.close()
"""


def main():
	print("Time:", time.strftime("%H:%M:%S", time.localtime(time.time())), sep="")
	ReadJson(settings.e2wGamePath + "/AppMonitor/" + settings.mkPath + "/results.json")
	print("SavePageWeb start Time:", time.strftime("%H:%M:%S", time.localtime(time.time())), sep="")
	SavePageWeb()#下载网页内容
	print("SavePageWeb end Time:", time.strftime("%H:%M:%S", time.localtime(time.time())), sep="")
	# print("SaveWebImage start Time:", time.strftime("%H:%M:%S", time.localtime(time.time())), sep="")
	# SaveWebImage()  # 截取网页图片
	# print("SaveWebImage end Time:", time.strftime("%H:%M:%S", time.localtime(time.time())), sep="")


if __name__ == '__main__':
	main()
