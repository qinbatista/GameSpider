# -*- coding: utf-8 -*-
import json
import os
import re
import chardet
from function import settings
def PythonLocation():
	return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
"""中间序列号整理"""
def PriorityRescreen():
	dict_key = {'S':[],'A':[],'B':[],'C':[],'D':[],'TBD':[]}
	dict1 = json.load(open(settings.e2wGamePath + "/GameList.json", encoding = GetEncoding(settings.e2wGamePath + "/GameList.json")))
	dict2 = json.load(open(settings.e2wGamePath + "/Cache/GP.json",encoding = GetEncoding(settings.e2wGamePath + "/Cache/GP.json")))
	for keys in dict2.keys():
		for values_key in dict2.get(keys):
			for k_values in dict1.keys():
				if k_values == values_key:
					for values_v in  dict1.get(k_values):
						if values_v.replace(" ","") != "":
							dict_key[keys].append(values_v)
	with open(settings.e2wGamePath + "/Cache/PriorityRescreen.json", 'w',encoding='utf-8') as out:
		json.dump(dict_key, out, ensure_ascii=False)#ensure_ascii=False 以中文形式输入
"""外层整理，游戏顺序整理"""
def SortGameOrder():
	dictEnd = {}
	dict1 = json.load(open(settings.e2wGamePath + "/Cache/PriorityRescreen.json", encoding = GetEncoding(settings.e2wGamePath + "/Cache/PriorityRescreen.json")))
	dict2 = json.load(open(settings.e2wGamePath + "/AppMonitor/" + settings.mkPath + "/results.json",encoding=GetEncoding(settings.e2wGamePath + "/AppMonitor/" + settings.mkPath + "/results.json")))
	Total = 0
	for key in dict1.keys():
		#storage Chinese Game
		for value_key in dict1.get(key):
			for v_key in dict2.keys():
				if v_key == value_key.replace("&"," ") and Chinese(v_key):
					dictEnd.update({v_key:dict2.get(v_key)})
		#storage English Game
		for value_key in dict1.get(key):
			for v_key in dict2.keys():
				if v_key == value_key and Chinese(v_key) == False:
					dictEnd.update({v_key:dict2.get(v_key)})
			if Total < len(dict2.get(value_key.replace("&",""))):#使用过&的游戏名在搜索时已经被替换了
				Total = len(dict2.get(value_key))
		dictEnd.update({key:[]})
	listEnd = []
	for a in range(Total):
		listEnd.append('15-')
	for key in dictEnd:
		if key in dict1.keys():
			dictEnd.update({key:listEnd})
	with open(settings.e2wGamePath + "/AppMonitor/" + settings.mkPath + "/results.json", 'w',encoding='utf-8') as out:
		json.dump(dictEnd, out, ensure_ascii=False)#ensure_ascii=False 以中文形式输入
	os.remove(settings.e2wGamePath + "/Cache/PriorityRescreen.json")
def GetEncoding(_Path):
	myfile = open(_Path,'rb')
	data = myfile.read()
	di= chardet.detect(data)
	myfile.close()
	myencoding = di["encoding"]
	if myencoding==None:
		myencoding ="utf-8"
	return myencoding
def Chinese(contents):#汉字识别
	Chinese = re.compile('[\u4e00-\u9fa5]')
	a = Chinese.search(contents)
	if a:
		return True
	else:
		return False
"""内层整理，Order方法使每个游戏内部进行渠道排序整理"""
def Order(SpiderName_list:list):
	dict1 = json.load(open(settings.e2wGamePath + "/AppMonitor/" + settings.mkPath + "/results_log.json",encoding=GetEncoding(settings.e2wGamePath + "/AppMonitor/" + settings.mkPath + "/results_log.json")))
	# for d in dict1:
	# 	print(d)
	# with open(settings.e2wGamePath + "/AppMonitor/" + settings.mkPath + "/results_log.json", 'w',encoding='utf-8') as out:
	# 	json.dump(dict1, out, ensure_ascii=False)#ensure_ascii=False 以中文形式输入
	for key in dict1.keys():
		list_end = []
		dict1_list = dict1.get(key)
		for SpiderName in SpiderName_list:#SpiderName_list为渠道列表
			for i in range(len(dict1_list)):
				if SpiderName == dict1_list[i] and dict1_list[i] not in list_end:
					list_end.append(dict1_list[i])
					list_end.append(dict1_list[i+1])
		dict1[key] = list_end
	with open(settings.e2wGamePath + "/AppMonitor/" + settings.mkPath + "/results.json", 'w',encoding='utf-8') as out:
		json.dump(dict1, out, ensure_ascii=False)#ensure_ascii=False 以中文形式输入

def main(SpiderName_list:list):
	print(SpiderName_list)
	Order(SpiderName_list)#整理每个游戏内部的渠道顺序
	PriorityRescreen()#中间序列号整理
	SortGameOrder()#整理每个游戏顺序

#此方法仅供开发者测试用
def test():
	tdict = json.load(open(settings.e2wGamePath + "/AppMonitor/" + settings.mkPath + "/results.json", encoding=GetEncoding(settings.e2wGamePath + "/AppMonitor/" + settings.mkPath + "/results.json")))
	n = 0
	for key in tdict.keys():
		if n != len(tdict.get(key)):
			n = len(tdict.get(key))
			print(len(tdict.get(key)))

if __name__ == '__main__':
	# test()#此方法仅供开发者测试用
	main(['OPPO', '小米', '魅族', '4399App', '4399_PC', '华为应用市场', 'VIVO', '豌豆荚', '乐视', 'TapTap', 'BILIBILI', '360', '应用宝', '百度游戏_App', '安智', '金立', '今日头条', '游迅网', '虫虫游戏', '酷酷跑', '拇指玩', 'PC6', '丫丫玩', 'TT玩', '木蚂蚁', '优亿市场', '7小7手游', '怪猫游戏平台', '游品味', '聚乐游戏中心', '葫芦侠', '纽扣助手', '9k9k', '九游', '当乐网', '乐嗨嗨', '吾爱安卓游戏', 'GG助手', '果盘游戏', '熊猫玩', '搜狗', '49you', '97973手游网', '东品游戏'])
