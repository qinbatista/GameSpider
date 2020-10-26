# -*- coding: utf-8 -*-
import json
from function import spiders,QinExcel,PriorityRescreen,settings,DownloadPage,GamePriority
from collections import defaultdict
import os
import time,random
import chardet
import threading
Game_list=[]

def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))
# Set this line to True if you want verbose logging. This is useful to see which spiders are
# taking a long time to complete their search. (Default is False)
VERBOSE = True

# Set this line to False if you do not want colored terminal output. (Default is True)
COLORED = True

SPIDERS = [spiders.oppoSpider(),spiders.xiaomiSpider(), spiders.meizuSpider(),spiders._4399_AppSpider(), spiders._4399_PCSpider(),
			spiders.huaweiSpider(),spiders.vivoSpider(), spiders.WDJSpider(), spiders.taptapSpider(),
			spiders.bilibiliSpider(),spiders._360Spider(),spiders.MyAppSpider(),spiders.baiduSpider(), spiders.anzhiSpider(),spiders.GioneeSpider(),
			spiders.TouTiaoSpider(),
		spiders.yxdownSpider(), spiders.ccplaySpider(), spiders.kukupaoSpider(), spiders.muzhiwanSpider(),
		spiders.pc6Spider(), spiders.yayawanSpider(), spiders.tzshouyouSpider(), spiders.mumayiSpider(),
		spiders.eoemarketSpider(), spiders.x7sywSpider(), spiders.gm88Spider(), spiders.ypw163Spider(),
		spiders.joloplaySpider(), spiders.huluxiaSpider(), spiders.niucooSpider(), spiders._9k9kSpider(),
		spiders._9gameSpider(), spiders.dSpider(), spiders.lehihiSpider(), spiders._25gameSpider(),
		spiders.ggzhushouSpider(), spiders.guopanSpider(), spiders.xmwanSpider(),
		spiders.sogouSpider(), spiders._49youSpider(), spiders.sinaSpider(), spiders.e2wGameSpider(),
]
# save result list
results = defaultdict(list)
# Uncomment this line if you want to test a subset of the spiders.
# SPIDERS = [spiders.e2wGameSpider()]
'''
colors is a class that defines a few useful color escape sequences
for printing colored terminal output.
colors are working under the linux and macOS terminals.
uses ANSI color escape sequences
'''
class colors:
	GRN = '\033[92m' if COLORED else ''
	RED = '\033[91m' if COLORED else ''
	YLW = '\033[93m' if COLORED else ''
	PRP = '\033[35m' if COLORED else ''
	END = '\033[0m'  if COLORED else ''

def GetEncoding(_Path):
		myfile = open(_Path,'rb')
		data = myfile.read()
		di= chardet.detect(data)
		myfile.close()
		myencoding = di["encoding"]
		if myencoding==None:
			myencoding ="utf-8"
		return myencoding

'''
get_chinese_names() returns a list of chinese names of the games
found in the given dictionary.
'''
def get_chinese_names(folder_dict: dict) -> [str]:
	return [name[1] for name in folder_dict.values() if len(name) > 1]


'''
get_english_names() returns a list of english names of the games
found in the given dictionary.
'''
def get_english_names(folder_dict: dict) -> [str]:
	return [name[0] for name in folder_dict.values()]

'''
get_game_names() returns a list of all game names found in the given
json file
'''
def get_game_names(filename: str) -> [str]:
	d = json.load(open(filename, encoding = GetEncoding(filename)))
	return get_english_names(d) + get_chinese_names(d)

'''
write_json_to_file() writes the given dictionary to a json file at
the given location.
'''
def write_json_to_file(d: dict, filename: str) -> None:
	with open(filename, 'w', encoding='utf-8') as out:
		json.dump(d, out, ensure_ascii=False)


'''
search() uses each spider in the SPIDERS list and checks for the existence of the game given
by the key value. If a game is found, the url it was found at is added to the result dictionary.
'''

'''
Mythread use for create thread for each channel, join method will let thread to wait until all thread finished
'''
def search(key: str, result: defaultdict) -> None:
	#mulit thread
	threads = [SpiderThread(args=(spider,key,result)) for spider in SPIDERS]
	for t in threads:
		t.start()
	num = 1
	for t in threads:
		t.join()
		print("************************************* 已完成：%0.2f%% *************************************"%(float(num/len(threads))*100))
		num += 1
	return key

class SpiderThread(threading.Thread):
	def run(self):
		#each game have each thread to do all spider
		if self._args[0].hasGame(self._args[1]):#self._args=(类名,游戏名,空列表)
			#print('[' + colors.RED + 'FOUND' + colors.END + '] {}'.format(self._args[0].getUrl()))
			self._args[2][self._args[1]].append(self._args[0].SpiderName)
			self._args[2][self._args[1]].append(self._args[0].getUrl())
		else:
			self._args[2][self._args[1]].append(self._args[0].SpiderName)
			if not self._args[0].Accessible:
				self._args[2][self._args[1]].append("-")
			else:
				self._args[2][self._args[1]].append("")
			#print('[' + colors.YLW + 'NOT FOUND' + colors.END + '] {}'.format(self._args[0].getUrl()))

class PerfectThread(threading.Thread):
	def run(self):
		global Game_list
		isUrl = self._args[0].hasGame(self._args[1])# _args[0] = spiders, _args[1] = 游戏名
		num = 0
		while self._args[0].Accessible == False and num < 10:
			num += 1
			time.sleep(random.randint(1,10))
			isUrl = self._args[0].hasGame(self._args[1])
		if num == 10:
			print("渠道:",self._args[0].getSpiderName()," 游戏:",self._args[1],"    十次连接失败，该请求已经自动退出",sep="")
		for n in range(0,len(Game_list),3):
			if Game_list[n+1] == self._args[0].getSpiderName() and Game_list[n] == self._args[1]:
				Game_list[n+2] = self._args[0].getUrl() if isUrl else ""
				break

class Perfect:
	def __init__(self):
		global Game_list
		self.Results = {}
	def AnalysisDate(self,JsonLocation):
		self.AnalysisJson(JsonLocation,True)
		print("Perfect search for Start Time:",time.strftime("%H:%M:%S",time.localtime(time.time())),sep="")
		threads = []
		for n in range(0,len(Game_list),3):
			for spider in SPIDERS:
				if Game_list[n+1] == spider.getSpiderName():
					threads.append(PerfectThread(args=(spider, Game_list[n])))# _args[0] = spiders, _args[1] = 游戏名
					break
		for thread in threads:
			thread.start()
		num = 1
		for thread in threads:
			thread.join()
			print("************************************* 已完成：%0.2f%% *************************************"%(float(num/len(threads))*100))
			num = num + 1
		self.AnalysisJson(JsonLocation,False)
		write_json_to_file(self.Results, JsonLocation)
		print("Perfect search for End Time:",time.strftime("%H:%M:%S",time.localtime(time.time())),sep="")
	def AnalysisJson(self,JsonLocation,isRead):
		readed = json.load(open(JsonLocation, 'r',encoding=GetEncoding(JsonLocation)))
		self.Results = readed
		for game in readed:
			for n in range(0,len(readed[game]),2):
				if readed[game][n+1] == '-':
					if isRead:
						Game_list.append(game)#游戏名
						Game_list.append(readed[game][n])#渠道名
						Game_list.append('-')
					else:
						for gn in range(0,len(Game_list),3):
							if Game_list[gn] == game and Game_list[gn+1] == readed[game][n]:
								self.Results[game][n+1] = Game_list[gn+2]

def SinglaSearch(key):
	global SPIDERS
	gameName = key.replace("&", " ")
	settings.mkPath = "S_" + time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time()))
	#创建需要用到的文件夹
	######################## 以下部分为更新部分 #############################
	if not os.path.exists(settings.e2wGamePath + "/AppMonitor/" + settings.mkPath):
		os.mkdir(settings.e2wGamePath + "/AppMonitor/" + settings.mkPath)
	else:
		n = 0
		MymkPath = settings.mkPath + str(n)
		while os.path.exists(settings.e2wGamePath + "/AppMonitor/" + MymkPath):
			n += 1
			MymkPath = settings.mkPath + str(n)
		os.mkdir(settings.e2wGamePath + "/AppMonitor/" + MymkPath)
		settings.mkPath = MymkPath
	settings.mkPath_dict[gameName] = settings.mkPath
	if settings.StartGamePriority:
		GamePriority.main()
	k = search(gameName, results)
	######################## 以下部分尽量上锁 #############################
	singlg_results = {k:results[k]}
	write_json_to_file(singlg_results, settings.e2wGamePath + "/AppMonitor/" + settings.mkPath_dict[k] + "/results.json")
	print('Json writing done...')

	print("Perfect start Time:",time.strftime("%H:%M:%S",time.localtime(time.time())),sep="")
	if settings.StartPerfectSearch:#完善爬虫没有爬到的数据
		p = Perfect()
		p.AnalysisDate(settings.e2wGamePath + "/AppMonitor/" + settings.mkPath_dict[k] + "/results.json")
	print("Perfect end Time:",time.strftime("%H:%M:%S",time.localtime(time.time())),sep="")

	test = QinExcel.QinExcelClass()
	print('Creating excel file.....')
	test.AnalysisData(settings.e2wGamePath + "/AppMonitor/" + settings.mkPath_dict[k] + "/GamePublishList.xlsx",settings.e2wGamePath + "/AppMonitor/" + settings.mkPath_dict[k] + "/results.json")
	print('Created excel file.')
	if settings.StartDownloadPage:
		DownloadPage.main()
	settings.mkPath = settings.mkPath_dict[k]
	results.pop(k)
	settings.mkPath_dict.pop(k)
	return settings.mkPath

if __name__=='__main__':
	print("Time:",time.strftime("%H:%M:%S",time.localtime(time.time())),sep="")
	SinglaSearch(input("输入游戏名字:"))#Unkilled  Stack&Crack
	print("Time:",time.strftime("%H:%M:%S",time.localtime(time.time())),sep="")
