# -*- coding: utf-8 -*-
import json
import multiprocessing,asyncio
from function import spiders,QinExcel,PriorityRescreen,DownloadPage,GamePriority,settings,ExcelToJson
from collections import defaultdict
import os,random
import time
import chardet
import threading
Game_list = []#失败的游戏列表

# Set this line to True if you want verbose logging. This is useful to see which spiders are
# taking a long time to complete their search. (Default is False)
VERBOSE = True
SPIDERS = [spiders.oppoSpider(),spiders.xiaomiSpider(), spiders.meizuSpider(),spiders._4399_AppSpider(), spiders._4399_PCSpider(),
			spiders.huaweiSpider(),spiders.vivoSpider(), spiders.WDJSpider(), spiders.taptapSpider(),
			spiders.bilibiliSpider(),spiders._360Spider(),spiders.MyAppSpider(),spiders.baiduSpider(), spiders.anzhiSpider(),spiders.GioneeSpider(),
			spiders.TouTiaoSpider(),
		spiders.yxdownSpider(), spiders.ccplaySpider(), spiders.kukupaoSpider(), spiders.muzhiwanSpider(),
		spiders.pc6Spider(), spiders.yayawanSpider(), spiders.mumayiSpider(),
		spiders.eoemarketSpider(), spiders.gm88Spider(), spiders.ypw163Spider(),
		spiders.joloplaySpider(), spiders.huluxiaSpider(), spiders.niucooSpider(), spiders._9k9kSpider(),
		spiders._9gameSpider(), spiders.dSpider(), spiders.lehihiSpider(), spiders._25gameSpider(),
		spiders.ggzhushouSpider(), spiders.guopanSpider(), spiders.xmwanSpider(),
		spiders.sogouSpider(), spiders._49youSpider(), spiders.sinaSpider(), spiders.e2wGameSpider(),
]
# Uncomment this line if you want to test a subset of the spiders.
# SPIDERS = [spiders.sogouSpider()
# ]
# save result list
results = defaultdict(list)
results_perfect = {}
SpiderName_list = []
thread_start_num = 60#每次开启的游戏搜索数量0
'''
colors is a class that defines a few useful color escape sequences
for printing colored terminal output.
colors are working under the linux and macOS terminals.
uses ANSI color escape sequences
'''
class colors:
	GRN = '\033[92m' if settings.COLORED else ''
	RED = '\033[91m' if settings.COLORED else ''
	YLW = '\033[93m' if settings.COLORED else ''
	PRP = '\033[35m' if settings.COLORED else ''
	END = '\033[0m'  if settings.COLORED else ''

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
def search(key: str) -> None:
	#mulit thread
	threads = [SpiderThread(args=(spider,key)) for spider in SPIDERS]
	for t in threads:
		t.start()
	for t in threads:
		t.join()

class SpiderThread(threading.Thread):
	def run(self):
		#each game have each thread to do all spider
		isTrue = self._args[0].hasGame(self._args[1])
		self.mutex = threading.Lock()
		self.mutex.acquire()
		global results
		if isTrue:
			results[self._args[1]].append(self._args[0].SpiderName)
			results[self._args[1]].append(self._args[0].getUrl())
		else:
			results[self._args[1]].append(self._args[0].SpiderName)
			results[self._args[1]].append("" if self._args[0].Accessible else "-")
		self.mutex.release()

class MyThread(threading.Thread):
	def run(self):
		search(self._args[0])


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
	def __init__(self, JsonLocation):
		global Game_list
		self.JsonLocation = JsonLocation
		self.results_perfect = {}
	def AnalysisDate(self):
		self.AnalysisJson(True)
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
			num += 1
		print("************************************* " + colors.GRN + "Perfect 已完成：100.00%%" + colors.END + " *************************************")
		self.AnalysisJson(False)
		write_json_to_file(self.results_perfect, self.JsonLocation)
		print("Perfect search for End Time:",time.strftime("%H:%M:%S",time.localtime(time.time())),sep="")
	def AnalysisJson(self,is_read):
		readed = json.load(open(self.JsonLocation, 'r',encoding=GetEncoding(self.JsonLocation)))
		self.results_perfect = readed
		for game in readed:
			for n in range(0,len(readed[game]),2):
				if readed[game][n+1] == '-':
					if is_read:
						Game_list.append(game)#游戏名
						Game_list.append(readed[game][n])#渠道名
						Game_list.append('-')
					else:
						for gn in range(0,len(Game_list),3):
							if Game_list[gn] == game and Game_list[gn+1] == readed[game][n]:
								self.results_perfect[game][n+1] = Game_list[gn+2]

def GetGit():
	print("git提交中...")
	os.chdir(settings.Path + "/../../")
	os.system("git add .")
	os.system("git commit -m autoupdate")
	os.system("git push")

def run_thread(game_list,processes_num):
	global thread_start_num
	threads = [MyThread(args=(game,)) for game in game_list]
	thread_total_sum = len(threads)+len(threads)*len(SPIDERS)+1
	thread_each_num = (thread_start_num+thread_start_num*len(SPIDERS)+1 if (thread_start_num+thread_start_num*len(SPIDERS)+1 < thread_total_sum) else thread_total_sum)
	print("[进程%d] 游戏数量：%d\t渠道数量：%d\t每次线程开启的数量：%d\t此进程开启的总线程数量：%d"%(processes_num,len(threads),len(SPIDERS),thread_each_num,thread_total_sum))
	thread_start_list = []
	num = 0
	for t in threads:
		t.setDaemon(True)#Set the child thread to be a daemon thread, the main thread ends, and all child threads are terminated.
		t.start()
		thread_start_list.append(t)
		while len(thread_start_list) >= thread_start_num:
			for thread_join in thread_start_list:
				print("Time:",time.strftime("%H:%M:%S",time.localtime(time.time())),sep="")
				print("************************************* [进程%d] 已完成：%0.2f%% *************************************"%(processes_num,float(num/len(threads))*100))
				thread_join.join()
				num += 1
			thread_start_list = []
	if len(thread_start_list) != 0:
		for thread_join in thread_start_list:
			print("Time:",time.strftime("%H:%M:%S",time.localtime(time.time())),sep="")
			print("************************************* [进程%d] 已完成：%0.2f%% *************************************"%(processes_num,float(num/len(threads))*100))
			thread_join.join()
			num += 1
	print("************************************* " + colors.GRN + "[进程%d] 已完成：100.00%%"%processes_num + colors.END + " *************************************")
	return dict(results)

def run_search() -> None:
	settings.mkPath = "A_" + time.strftime("%Y%m%d_%H%M%S",time.localtime(time.time()))
	#创建需要用到的文件夹
	os.mkdir(settings.e2wGamePath + "/AppMonitor/" + settings.mkPath)
	if settings.StartGamePriority:
		GamePriority.main()
	#Create thread for each game
	games = get_game_names(settings.e2wGamePath + "/GameList.json")
	#筛选games，防止重复，防止无中文游戏
	games_n = []
	for game in games:
		if game not in games_n and game.replace(" ","") != "":
			games_n.append(game.replace("&",""))
	games = games_n
	######################################################################
	thread_total_sum = len(games) * (len(SPIDERS) + 1) + settings.Processes + 1
	print("游戏总数量：%d\t\t渠道总数量：%d"%(len(games),len(SPIDERS)))
	print("可用进程数：%d\t\t线程总数量：%d\n"%(settings.Processes,thread_total_sum))
	pool_list = []
	#添加进程带领线程跑
	pool = multiprocessing.Pool(processes=settings.Processes)
	mold = len(games)//settings.Processes if len(games) % settings.Processes == 0 else (len(games)//settings.Processes + 1)
	for i in range(settings.Processes):
		if len(games[mold * i:mold * ( i + 1 )]) == 0:break
		pool_list.append(pool.apply_async(run_thread, (games[mold * i:mold * ( i + 1 )],i)))
	pool.close()
	pool.join()
	for pool_dict in pool_list:
		results.update(pool_dict.get())
	######################################################################
	print('[' + colors.GRN + 'FINISHED' + colors.END + ']')
	print('Writing results to file.....', end = '')
	write_json_to_file(results, settings.e2wGamePath + "/AppMonitor/" + settings.mkPath + "/results.json")
	write_json_to_file(results, settings.e2wGamePath + "/AppMonitor/" + settings.mkPath + "/results_log.json")######  检验PriorityRescreen方法是否排序错误的文档  ######
	print('Json writing done...')
	#get Spider Name
	global SpiderName_list
	for spider in SPIDERS:
		SpiderName_list.append(spider.getSpiderName())
	print("PriorityRescreen start Time:",time.strftime("%H:%M:%S",time.localtime(time.time())),sep="")
	# PriorityRescreen为游戏排序模板
	PriorityRescreen.main(SpiderName_list)#Reordering
	print("PriorityRescreen end Time:",time.strftime("%H:%M:%S",time.localtime(time.time())),sep="")

	print("Perfect start Time:",time.strftime("%H:%M:%S",time.localtime(time.time())),sep="")
	if settings.StartPerfectSearch:#完善爬虫没有爬到的数据
		Perfect(settings.e2wGamePath + "/AppMonitor/" + settings.mkPath + "/results.json").AnalysisDate()
	print("Perfect end Time:",time.strftime("%H:%M:%S",time.localtime(time.time())),sep="")

	test = QinExcel.QinExcelClass()
	print("Creating excel start Time:",time.strftime("%H:%M:%S",time.localtime(time.time())),sep="")
	print('Creating excel file.....')
	test.AnalysisData(settings.e2wGamePath + "/AppMonitor/" + settings.mkPath + "/GamePublishList.xlsx",settings.e2wGamePath + "/AppMonitor/" + settings.mkPath + "/results.json")
	print('Created excel file.')
	print("Creating excel end Time:",time.strftime("%H:%M:%S",time.localtime(time.time())),sep="")
	if settings.StartDownloadPage:DownloadPage.main()
	if settings.StartGit:GetGit()

if __name__=='__main__':
	print("StartSearch start Time:",time.strftime("%H:%M:%S",time.localtime(time.time())),sep="")
	run_search()
	print("StartSearch end Time:",time.strftime("%H:%M:%S",time.localtime(time.time())),sep="")

	# n = 6
	# while n > 0:
	# 	n = n - 1
	# 	print("Time:",time.strftime("%H:%M:%S",time.localtime(time.time())),sep="")
	# 	run_search()
	# 	print("Time:",time.strftime("%H:%M:%S",time.localtime(time.time())),sep="")
	# 	time.sleep(666)