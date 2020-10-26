# -*- coding: utf-8 -*-
# spiders.py                     #
#                                #
# Matthew Fernandez              #
# Qin                            #
##################################
import json
import threading
import time
import urllib
import urllib.parse
import urllib.request
from random import choice

import re
import requests
from bs4 import BeautifulSoup
from function import settings
from xpinyin import Pinyin

#the dely time of accessing web
WaitingTime = 1
'''
Spider defines a base class for a web spider who's goal is to check
whether or not a specified game exists on the website.
Each website spider should derive itself from this base class.
For most websites, the _decode_response and hasGame methods do
not need to be overriden, however on occasion they might need to be.
'''
#字体颜色设置
class colors:
	GRN = '\033[92m'
	RED = '\033[91m'
	YLW = '\033[93m'
	PRP = '\033[35m'
	END = '\033[0m'
class Spider:
	def __init__(self, spiderName):
		self.mutex = threading.Lock()
		self.SpiderName = spiderName
		self.Accessible = True
		self.WaitingTime = WaitingTime
		self.baseurl = None
	def getUrl(self) -> str:
		return self.baseurl
	def post(self,url,data=None) -> requests:
		try:response = requests.post(url,headers = {'User-Agent':choice(settings.AGENTS)},data=data,proxies = (choice(settings.proxies_list) if settings.StartProxies else {}),timeout = 30)
		except:
			response = requests.post(url,headers = {'User-Agent':choice(settings.AGENTS)},data=data,timeout = 30)
			print(colors.YLW + "警告！" + colors.END + self.getSpiderName() + "渠道 --- 找不到setting文件下的StartProxies关键字或proxies_list列表！",sep="")
		return response
	def get(self,url) -> requests:
		try:response = requests.get(url,headers = {'User-Agent':choice(settings.AGENTS)},proxies = (choice(settings.proxies_list) if settings.StartProxies else {}),timeout = 30)
		except:
			response = requests.get(url,headers = {'User-Agent':choice(settings.AGENTS)},timeout = 30)
			print(colors.YLW + "警告！" + colors.END + self.getSpiderName() + "渠道 --- 找不到setting文件下的StartProxies关键字或proxies_list列表！",sep="")
		return response
	def getSpiderName(self) -> str:
		return self.SpiderName

"""---------------------------------------------新增渠道爬虫---------------------------------------------"""
#oppoSpider可能需要优化，此处为耗时的主要渠道，OPPO不能用代理
class oppoSpider(Spider):
	def __init__(self):
		Spider.__init__(self, "OPPO")
		self.urlnum = 0
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		k = '0'#判断访问页面是否为最后一页，为最后一页，服务器返回1，否则服务器返回0
		self.urlnum = 0#流动页数递增访问
		self.Accessible=True
		try:
			while k == '0':
				url = "https://app.cdo.oppomobile.com/home/game/index.json?" + urllib.parse.urlencode([('start', self.urlnum)])
				self.urlnum += 1#流动页数递增访问
				response = self.get(url)
				dict_s = json.loads(response.text,encoding="utf-8")
				k = str(dict_s.get('data').get('isEnd'))
				cards_list = dict_s.get('data').get('cards')
				for cards_dict in cards_list:
					for cards_dict_dict in cards_dict.get('apps'):
						if key in cards_dict_dict.get('appName'):
							self.baseurl = url
							return True
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class e2wGameSpider(Spider):
	def __init__(self):
		Spider.__init__(self, "东品游戏")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "http://www.gamer-gamer.com/gamergamer/index.php?g=portal&m=search&a=index"
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.post(url,data = {'keyword' : key})
			try:
				soup = BeautifulSoup(response.text.encode('utf-8'),features='html.parser')
				div_list = soup.find('div',{"class":"span9"}).find_all('div',{"class":"tc-gridbox"})
				for div in div_list:
					a = div.find("a")
					name = a.find("img").get("alt").replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k == name:
						self.baseurl = 'http://www.gamer-gamer.com/' + a.get('href')
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class taptapSpider(Spider):
	def __init__(self):
		Spider.__init__(self, "TapTap")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "https://www.taptap.com/search/" + urllib.parse.quote(key)
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				soup = BeautifulSoup(response.text.encode('utf-8'),features='html.parser')
				div_list = soup.find_all('div',{"class":"taptap-app-card"})
				for div in div_list:
					a = div.find("a")
					title = a.find("img").get("title").replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if title == k:
						self.baseurl = a.get('href')
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class xiaomiSpider(Spider):
	def __init__(self):
		Spider.__init__(self, "小米")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "https://game.wali.com/search/" + urllib.parse.quote(key)
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				soup = BeautifulSoup(response.text.encode('utf-8'),features='html.parser')
				div_list = soup.find("div",{"class":"game-item-list"}).find_all("div",{"class":"game-detail-wrapper clearfix"})
				for div in div_list:
					text = div.find("div",{"class":"clearfix game-about-container"}).find("span").text
					text = text.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if text == k:
						self.baseurl = url
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class _4399_AppSpider(Spider):
	def __init__(self):
		Spider.__init__(self, "4399App")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "http://a.4399.cn/mobile/ajax/search-index.html?key=" + urllib.parse.quote(key)
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				dict_s = json.loads(response.text,encoding="utf-8")
				list_s = dict_s.get('list')
				for list_key in list_s:
					text = list_key.get('title').replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k == text:
						self.baseurl = "http://a.4399.cn" + list_key.get('wap_url')
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class WDJSpider(Spider):
	def __init__(self):
		Spider.__init__(self, "豌豆荚")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "https://www.wandoujia.com/search?key=" + urllib.parse.quote(key)
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				soup = BeautifulSoup(response.text.encode('utf-8'),features='html.parser')
				ul = soup.find("ul",{"id":"j-search-list"})
				li_list = ul.find_all("li",{"class":"search-item search-searchitems"})
				for li in li_list:
					a = li.find("h2",{"class":"app-title-h2"}).find("a")
					text = a.text.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if text == k:
						self.baseurl = a.get("href")
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class LetvSpider(Spider):
	def __init__(self):
		Spider.__init__(self, "乐视")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "http://mobile.leplay.cn/baseapi/mapi/search/list?wd=" + urllib.parse.quote(key)
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				dict = json.loads(response.text,encoding="utf-8")
				items = dict.get('entity').get('items')
				for item in items:
					name = item.get("name").replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					self.baseurl = "http://mobile.leplay.cn/app/" + str(item.get("id"))
					if k in name:
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class baiduSpider(Spider):
	def __init__(self):
		Spider.__init__(self, "百度游戏")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "http://g.baidu.com/a/search.json"
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.post(url,data={"keyword":key,"page":"1"})
			try:
				response = json.loads(response.content.decode(encoding = 'utf-8'))
				for item in response['data']['gameList']:
					name = item.get("name").replace("<em>","").replace("</em>","").replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k == name:
						gameNameShort = item.get("gameNameShort")
						self.baseurl = "http://g.baidu.com/a/" + gameNameShort
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible = False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible = False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class TouTiaoSpider(Spider):
	def __init__(self):
		Spider.__init__(self, "今日头条")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "https://ic.snssdk.com/game_channel/api/search_content?keyword=" + urllib.parse.quote(key)
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				dict_s = json.loads(response.text,encoding="utf-8")
				for game in dict_s['data']['game_list']:
					name = game.get('name').replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k == name:
						self.baseurl = game.get("download_info").get("pkg_name")
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class GioneeSpider(Spider):
	def __init__(self):
		Spider.__init__(self, "金立")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "http://game.gionee.com/search/list?t_bi=_1630755553&keyword="+urllib.parse.quote(key)+"&intersrc=isearch"
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				response.encoding = "utf-8"
				soup = BeautifulSoup(response.text,"html.parser")
				li_list = soup.find("ul",{"class":"game_list clearfix"}).find_all("li")
				for li in li_list:#ISO-8859-1
					a = li.find("h4").find("a")
					name = a.get("title").replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if name == k:
						self.baseurl = a.get("href")
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class _360Spider(Spider):
	def __init__(self):
		Spider.__init__(self, "360")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "http://u.360.cn/search/search/?key_word=" + urllib.parse.quote(key)
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				response.encoding = "utf-8"
				soup = BeautifulSoup(response.text,'html.parser')
				ul = soup.find('ul',{'class':'serlists'})
				li_list = ul.find_all('li')
				for li in li_list:
					a = li.find('strong').find('a',{'target':'_blank'})
					name = a.text.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if name in k or k in name:
						self.baseurl = a.get("href")
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class MyAppSpider(Spider):
	def __init__(self):
		Spider.__init__(self, "应用宝")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "https://android.myapp.com/myapp/searchAjax.htm?kw="+ urllib.parse.quote(key) + "&pns=&sid="
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			result = json.loads(self.post(url).text,encoding="utf-8")
			num = 3
			while not result["success"] and num:
				num -= 1
				result = json.loads(self.post(url).text,encoding="utf-8")
			try:
				items = result["obj"]["items"]
				for item in items:
					name = item["appDetail"]["appName"].replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					self.baseurl = "https://android.myapp.com/myapp/detail.htm?apkName=" + item["pkgName"]
					if name in k or k in name:
						self.baseurl = "https://android.myapp.com/myapp/detail.htm?apkName=" + item["pkgName"]
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
"""-----------------------------------------打开网页的渠道爬虫-------------------------------------------"""
"""-----------------------------------------暂时未写完的渠道爬虫-----------------------------------------"""
"""-----------------------------------------已写完在监控中的渠道爬虫-------------------------------------"""
"""-----------------------------------------------------------------------------------------------------"""
class sogouSpider(Spider):
	def __init__(self):
		Spider.__init__(self, "搜狗")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "https://wan.sogou.com/ajax/search/gamesearch.do?" + urllib.parse.urlencode([('q', key), ('pageSize', '5')])
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				result = json.loads(response.text,encoding="utf-8")
				games = result["result"]["games"]
				for game in games:
					name = re.sub("<.*?>","",game["name"]).replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k in name:
						self.baseurl = "http://wan.sogou.com/" + game["gid"]
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class _4399_PCSpider(Spider):
	def __init__(self):
		Spider.__init__(self,"4399_PC")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "http://so2.4399.com/search/search.php?" + urllib.parse.urlencode([('k', key)] , encoding = 'gb2312')
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			req = urllib.request.Request(url, headers = {'User-Agent' : choice(settings.AGENTS)})
			response = urllib.request.urlopen(req,timeout=5)
			try:html = response.read().decode(encoding = 'gb18030')
			except:html = response.read().decode(encoding = 'gb2312')
			try:
				soup = BeautifulSoup(html,features='html.parser')#ISO-8859-1
				a_list = soup.find_all("a",{"class":"fl_img"})
				for a in a_list:
					name = a.find("img").get("alt").replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k == name:
						self.baseurl = a.get("href")
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class yxdownSpider(Spider):
	def __init__(self):
		Spider.__init__(self,"游迅网")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "http://www.yxdown.com/searchsy?" + urllib.parse.urlencode([('sort', 'size'), ('wd', key)])
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				soup = BeautifulSoup(response.text.encode('utf-8'),features='html.parser')
				div_list = soup.find("div",{"class":"search_result"}).find_all("div",{"class":"result_list"})
				for div in div_list:
					a = div.find("div",{"class":"img_sy"}).find("a")
					name = a.find("img").get("alt")
					name = name.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k == name:
						url = a.get("href")
						if "http" not in url:
							url = "http://www.yxdown.com" + url
						self.baseurl = url
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class ccplaySpider(Spider):
	def __init__(self):
		Spider.__init__(self, "虫虫游戏")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "http://www.ccplay.cc/search/?" + urllib.parse.urlencode([('headKeywords', key), ('q', key)])
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				soup = BeautifulSoup(response.text.encode('utf-8'),features='html.parser')
				div_list = soup.find_all("div",{"class":"sort_item_content"})
				for div in div_list:
					p = div.find("p",{"class":"sort_item_name txt_overflow"})
					name = p.text.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k == name:
						self.baseurl = p.find("a").get("href")
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class kukupaoSpider(Spider):
	def __init__(self):
		Spider.__init__(self, "酷酷跑")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "https://www.kukupao.com/category/p1/" + urllib.parse.quote(key)
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				soup = BeautifulSoup(response.text.encode('utf-8'),features='html.parser')
				div_list = soup.find("div",{"id":"search-result"}).find_all("div",{"class":"m cf "})
				for div in div_list:
					a = div.find("div",{"class":"tit cf"}).find("a")
					name = a.get("title").replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k == name:
						self.baseurl = a.get("href")
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class huaweiSpider(Spider):
	def __init__(self):
		Spider.__init__(self,"华为应用市场")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "http://appstore.huawei.com/search/" + urllib.parse.quote(key)
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				soup = BeautifulSoup(response.text.encode("ISO-8859-1"),features='html.parser')
				div_list = soup.find_all("div",{"class":"game-info-ico"})
				for div in div_list:
					a = div.find("a")
					name = a.get("title").replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k == name:
						self.baseurl = "http://a.vmall.com/uowap/index.html#/detailApp" + a.get("href")[4:]
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class muzhiwanSpider(Spider):
	def __init__(self):
		Spider.__init__(self, "拇指玩")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "https://www.muzhiwan.com/search.html?" + urllib.parse.urlencode([('q', key)])
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				soup = BeautifulSoup(response.text.encode('utf-8'),features='html.parser')
				li_list = soup.find("div",{"class":"item-list"}).find("ul",{"class":"clearfix"}).find_all("li",{"class":"clearfix"})
				for li in li_list:
					a = li.find("div",{"class":"list-content"}).find("h6").find("a")
					name = a.text.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k == name:
						self.baseurl = "https://www.muzhiwan.com" + a.get("href")
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class pc6Spider(Spider):
	def __init__(self):
		Spider.__init__(self, "PC6")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "https://s.pc6.com/?cid=mobileGame&" + urllib.parse.urlencode([('k', key)])
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				soup = BeautifulSoup(response.text.encode('utf-8'),features='html.parser')
				dt_list = soup.find("dl",{"id":"result"}).find_all("dt")
				for dt in dt_list:
					a = dt.find("a")
					name = a.text.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k in name:
						self.baseurl = a.get("href")
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class yayawanSpider(Spider):
	def __init__(self):
		Spider.__init__(self,"丫丫玩")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "http://so.yayawan.com/app/?" + urllib.parse.urlencode([('k', key)])
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				soup = BeautifulSoup(response.text.encode('utf-8'),features='html.parser')
				li_list = soup.find("div",{"class":"list"}).find_all("li")
				for li in li_list:
					a = li.find("h3").find("a")
					# url = a.get("href")##########################################注释该语句可得到另一个网址
					name = a.find("em").text.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k == name:
						self.baseurl = url
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class tzshouyouSpider(Spider):
	def __init__(self):
		Spider.__init__(self, "TT玩")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "http://www.tzshouyou.com/index.php?" + urllib.parse.urlencode([('ac', 'search'), ('keyword', key)])
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				soup = BeautifulSoup(response.text.encode('ISO-8859-1'),features='html.parser')
				a_list = soup.find_all("a",{"class":"dg_icon_Search"})
				for a in a_list:
					name = a.find("img").get("alt").replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k == name:
						self.baseurl = a.get("href")
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class mumayiSpider(Spider):
	def __init__(self):
		Spider.__init__(self,"木蚂蚁")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "http://s.mumayi.com/index.php?" + urllib.parse.urlencode([('q', key)])
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				soup = BeautifulSoup(response.text.encode('utf-8'),features='html.parser')
				li_list = soup.find("ul",{"class":"applist"}).find_all("li",{"class":"iapp"})
				for li in li_list:
					a = li.find("a")
					name = a.get("alt").replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k == name:
						self.baseurl = a.get("href")
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class eoemarketSpider(Spider):
	def __init__(self):
		Spider.__init__(self,"优亿市场")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "http://www.eoemarket.com/search_.html?" + urllib.parse.urlencode([('keyword', key)])
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				soup = BeautifulSoup(response.text.encode('utf-8'),features='html.parser')
				div_list = soup.find_all("div",{"class":"Rlist"})
				for div in div_list:
					a = div.find("a")
					name = a.find("img").get("alt").replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k == name:
						self.baseurl = "http://www.eoemarket.com" + a.get("href")
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class _9k9kSpider(Spider):
	def __init__(self):
		Spider.__init__(self,"9k9k")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			pinj = ""
			for p in key:
				pinj = pinj + Pinyin().get_pinyin(p)[0]
			pin = Pinyin().get_pinyin(key).replace("-","")
			url = "https://www.9k9k.com/shouyou/" + pinj
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				soup = BeautifulSoup(response.text.encode('utf-8'),features='html.parser')
				name = soup.find("h1",{"class":"game_name"}).text.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
				if k == name:
					self.baseurl = url
					return True
				else:
					url = "https://www.9k9k.com/shouyou/" + pin
					response = self.get(url)
					soup = BeautifulSoup(response.text.encode('utf-8'),features='html.parser')
					name = soup.find("h1",{"class":"game_name"}).text.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k == name:
						self.baseurl = url
						return True
			except:	pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class vivoSpider(Spider):
	def __init__(self):
		Spider.__init__(self,"VIVO")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "http://search.gamecenter.vivo.com.cn/clientRequest/searchGame?" + urllib.parse.urlencode([('appVersionName', '2.0.1'), ('origin', '87'), ('adrVerName', '6.0.1'), ('search', key), ('cs', '0'), ('pixel', '2.0'), ('av', '23'), ('patch_sup', '1'), ('appVersion', '38'), ('imei', '863657034984347'), ('page_index', '1'), ('model', 'Redmi 3S'), ('s', '2|2544206749')])
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				response = json.loads(response.text, encoding = 'utf-8')
				for item in response['msg']:
					name = item['name'].replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k == name:
						self.baseurl = "https://game.vivo.com.cn/?cid=w-2-360-sem-qt#/detail/" + str(item['id'])
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class bilibiliSpider(Spider):
	def __init__(self):
		Spider.__init__(self,"BILIBILI_App")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "http://line3-h5-mobile-api.biligame.com/game/center/h5/search/page?" + urllib.parse.urlencode([('sdk_type', '1'), ('keyword', key), ('build', ''), ('mid', '0'), ('cur_host', 'app')])
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				for item in json.loads(response.text,encoding = 'utf-8')['data']['list']:
					name = item['title'].replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k == name:
						self.baseurl = item["download_link"]
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class huluxiaSpider(Spider):
	def __init__(self):
		Spider.__init__(self, "葫芦侠_App")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "http://search.huluxia.com/game/search/ANDROID/1.1?" + urllib.parse.urlencode([('platform', '2'), ('keyword', key)])
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				for item in json.loads(response.text,encoding = 'utf-8')['gameapps']:
					name = item['apptitle'].replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k == name:
						self.baseurl = item["localurl"]["url"]
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class ypw163Spider(Spider):
	def __init__(self):
		Spider.__init__(self, "游品味_App")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "http://ypw.163.com/api/v2/search?" + urllib.parse.urlencode([('query', key), ('limit', '10'), ('offset', '0')])
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				games = json.loads(response.text,encoding = 'utf-8')["games"]
				for game in games:
					name = game["name_cn"].replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k == name:
						self.baseurl = game["packs"][0]["cdn_apk_url"]#game["share_url"]
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class niucooSpider(Spider):
	def __init__(self):
		Spider.__init__(self, "纽扣助手_App")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "http://www.niucoo.cn/api/app/search.api?" + urllib.parse.urlencode([('key', key), ('pageSize', '10'), ('currentPage', '1'), ('version', '47')])
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.post(url,data={"key":key,"pageSize":"10","currentPage":"1","version":"47"})
			try:
				for item in json.loads(response.content.decode(encoding = 'utf-8'))['content']['data']:
					name = item['appName'].replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k in name:
						self.baseurl = item["linkBaidu"]
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
		finally:
			self.mutex.release()
class anzhiSpider(Spider):
	def __init__(self):
		Spider.__init__(self, "安智")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "http://www.anzhi.com/search.php?" + urllib.parse.urlencode([('keyword', key)])
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				soup = BeautifulSoup(response.text.encode('utf-8'),features='html.parser')
				li_list = soup.find("div",{"class":"app_list border_three"}).find("ul").find_all("li")
				for li in li_list:
					a = li.find("span",{"class":"app_name"}).find("a")
					name = a.text.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k == name:
						self.baseurl = "http://www.anzhi.com" + a.get("href")
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class x7sywSpider(Spider):
	def __init__(self):
		Spider.__init__(self, "7小7手游")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "http://www.x7syw.com/index.php?" + urllib.parse.urlencode([('ac', 'search'), ('keyword', key)])
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				soup = BeautifulSoup(response.text.encode('ISO-8859-1'),features='html.parser')
				li_list = soup.find("div",{"id":"tabcontentSearch"}).find("ul").find_all("li",{"class":"dangge-appSearch clearfix"})
				for li in li_list:
					a = li.find("a",{"class":"dg_icon_Search"})
					name = a.find("img").get("alt").replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k == name:
						self.baseurl = a.get("href")
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class gm88Spider(Spider):
	def __init__(self):
		Spider.__init__(self, "怪猫游戏平台")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "https://gm88.com/index.php?" + urllib.parse.urlencode([('app', 'game'), ('act', 'search'), ('keyword', key)])
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				soup = BeautifulSoup(response.text.encode('utf-8'),features='html.parser')#ISO-8859-1
				div_list = soup.find("div",{"class":"game_list_container"}).find_all("div",{"class":"core"})
				for div in div_list:
					a = div.find("div",{"class":"core-outer-message"}).find("a")
					name = a.find("p",{"class":"game-name"}).text.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k == name:
						self.baseurl = "https://gm88.com/" + a.get("href")
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class _9gameSpider(Spider):
	def __init__(self):
		Spider.__init__(self, "九游")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "http://www.9game.cn/search/?" + urllib.parse.urlencode([('keyword', key)],[("platformId", "2")])
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				soup = BeautifulSoup(response.text.encode('utf-8'),features='html.parser')#ISO-8859-1
				div_list = soup.find_all("div",{"class":"sr-poker"})
				for div in div_list:
					a = div.find("div",{"class":"left-con"}).find("a",{"class":"pic"})
					name = a.find("img").get("alt").replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k == name:
						self.baseurl = a.get("href")
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class dSpider(Spider):
	def __init__(self):
		Spider.__init__(self, "当乐网")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "http://android.d.cn/search/app/?" + urllib.parse.urlencode([('keyword', key)])
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				soup = BeautifulSoup(response.text.encode('utf-8'),features='html.parser')#ISO-8859-1
				div_list = soup.find_all("a",{"class":"app-img-out"})
				for a in div_list:
					name = a.find("img").get("alt").replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k == name:
						self.baseurl = a.get("href")
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class joloplaySpider(Spider):
	def __init__(self):
		Spider.__init__(self, "聚乐游戏中心")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "http://m.joloplay.com/searchpage.html?" + urllib.parse.urlencode([('keyword', key)]) + '#'
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				soup = BeautifulSoup(response.text.encode('utf-8'),features='html.parser')#ISO-8859-1
				a_list = soup.find("div",{"class":"djtj_list"}).find("ul").find_all("a",{"class":"img"})
				for a in a_list:
					name = a.get("title").replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k == name:
						self.baseurl = a.get("href")
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class cr173Spider(Spider):
	def __init__(self):
		Spider.__init__(self, "西西软件园")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "http://so.cr173.com/search/d/" + urllib.parse.quote(key) + "_all_hits.html"
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				soup = BeautifulSoup(response.text.encode('ISO-8859-1'),features='html.parser')#ISO-8859-1
				dl_list = soup.find_all("dl",{"class":"g-dl-top"})
				for dl in dl_list:
					a = dl.find("a")
					name = a.text.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k in name:
						self.baseurl = a.get("href")
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class _25gameSpider(Spider):#存在延迟性问题
	def __init__(self):
		Spider.__init__(self, "吾爱安卓游戏")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "https://www.25game.com/game/?" + urllib.parse.urlencode([('key', key)])
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				soup = BeautifulSoup(response.text.encode('utf-8'),features='html.parser')#ISO-8859-1
				a_list = soup.find("ul",{"class":"app_list"}).find_all("a",{"class":"left user_icon"})
				for a in a_list:
					name = a.get("title").replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k in name:
						self.baseurl = "https://www.25game.com" + a.get("href")
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class guopanSpider(Spider):
	def __init__(self):
		Spider.__init__(self, "果盘游戏")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "http://www.guopan.cn/gcsearch/?" + urllib.parse.urlencode([('name', key), ('searchtype', '游戏')])
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				soup = BeautifulSoup(response.text.encode('utf-8'),features='html.parser')#ISO-8859-1
				div_list = soup.find("div",{"class":"wrap_serachResult cf"}).find_all("div",{"class":"result_pic"})
				for div in div_list:
					a = div.find("a")
					name = a.find("img").get("title").replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k in name:
						self.baseurl = a.get("href")
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class _49youSpider(Spider):
	def __init__(self):
		Spider.__init__(self, "49you")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			pinj = ""
			for p in key:
				pinj = pinj + Pinyin().get_pinyin(p)[0]
			pin = Pinyin().get_pinyin(key).replace("-","")
			url = "http://www.49app.com/" + pinj
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			try:
				soup = BeautifulSoup(response.text.encode('utf-8'),features='html.parser')
				name = soup.find("p",{"class":"yxxqinfo_name"}).text.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
				if k == name:
					self.baseurl = url
					return True
				else:
					url = "http://www.49app.com/" + pin
					response = self.get(url)
					soup = BeautifulSoup(response.text.encode('utf-8'),features='html.parser')
					name = soup.find("p",{"class":"yxxqinfo_name"}).text.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k == name:
						self.baseurl = url
						return True
			except:	pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class xmwanSpider(Spider):
	def __init__(self):
		Spider.__init__(self, "熊猫玩")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "https://xmwan.com/e/search/index.php"
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			data = {"show":"title","classid":"1,2","tempid":"1","keyboard":key,"Submit":""}
			response = self.post(url,data = data)
			try:
				soup = BeautifulSoup(response.content.decode(encoding = 'utf-8'),"html.parser")
				p_list = soup.find("ul",{"id":"ajax_loading_con"}).find_all("p",{"class":"tit"})
				for p in p_list:
					a = p.find("a")
					name = a.text.replace("\n","").replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					print(name)
					print("https://xmwan.com" + a.get("href"))
					if k in name:
						self.baseurl = "https://xmwan.com" + a.get("href")
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible = False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible = False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible = False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class lehihiSpider(Spider):
	def __init__(self):
		Spider.__init__(self, "乐嗨嗨")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "http://www.lehihi.com/index.php/Index/indexgamesearch/"
			data = {"s_type":"sou","s_wd":key}
			response = self.post(url,data=data)
			result = json.loads(response.content.decode(encoding = 'utf-8'))
			try:
				if result["data"]!="":
					k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					soup = BeautifulSoup(result["data"],"html.parser")
					a_list = soup.find("div",{"class":"games"}).find_all("a")
					for a in a_list:
						name = a.get("title").replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
						if k == name:
							self.baseurl = a.get("href")
							return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible = False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible = False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible = False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class sinaSpider(Spider):
	def __init__(self):
		Spider.__init__(self, "97973手游网")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "http://search.97973.com/guides/product"
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.post(url,data = {"keyword":key,"index":"1"})
			response.encoding = "utf-8"
			try:
				soup = BeautifulSoup(response.text,"html.parser")
				div_list = soup.find_all("div",{"class":"listbox"})
				for div in div_list:
					a = div.find("div",{"class":"detail"}).find("a")
					name = a.text.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k == name:
						self.baseurl = a.get("href")
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			self.Accessible = False
			return False
		except UnicodeDecodeError:
			self.Accessible = False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible = False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
class meizuSpider(Spider):
	def __init__(self):
		Spider.__init__(self,"魅族")
	def convert(self,s):
		s = s.replace(" ","")
		sq = s[:s.find("&#x")]
		sn = s[s.find("&#x")+3:]
		if sn != "" and len(sn) == 4:
			sn = sq + bytes(r'\u' + sn, 'ascii').decode('unicode_escape') # 把'957f'转换成b'\\u957f'
		else:sn=""
		return sn
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "http://app.meizu.com/apps/public/search/page?" + urllib.parse.urlencode([('cat_id', '1'), ('keyword', key), ('start', '0'), ('max', '18')])
			k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			response = self.get(url)
			result = json.loads(response.text,encoding="utf-8")
			try:
				result_list = result["value"]["list"]
				for r in result_list:
					strs = r["name"].rsplit(";")
					name = ""
					for s in strs:
						if s.find("&#x") != -1:
							name += self.convert(s)
						else:
							name += s
					name = name.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
					if k in name or name in k:
						self.baseurl = "http://app.meizu.com/apps/public/detail?package_name=" + r["package_name"]
						return True
			except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible = False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible = False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible = False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
######################################


class ggzhushouSpider(Spider):
	def __init__(self):
		Spider.__init__(self,"GG助手")
	def hasGame(self, key: str) -> bool:
		time.sleep(self.WaitingTime)
		self.mutex.acquire()
		self.Accessible=True
		try:
			url = "http://ggzhushou.cn/game/search/" + urllib.parse.quote(key)
			# k = key.replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			# try:response = requests.get(url,headers = {'User-Agent':choice(settings.AGENTS)},proxies = (choice(settings.proxies_list) if settings.StartProxies else {}),timeout = 20)
			# except:
			# 	response = requests.get(url,headers = {'User-Agent':choice(settings.AGENTS)},timeout = 20)
			# 	print(self.getSpiderName() + " --- 警告！找不到setting文件下的StartProxies关键字或proxies_list列表有误！")
			# try:
			# 	soup = BeautifulSoup(response.text.encode('utf-8'),features='html.parser')#ISO-8859-1
			# 	a_list = soup.find("ul",{"class":"app_list"}).find_all("a",{"class":"left user_icon"})
			# 	for a in a_list:
			# 		name = a.get("title").replace(":","").replace(" ","").replace("：","").replace("-","").replace("_","").replace("(","").replace(")","").replace("（","").replace("）","")
			# 		if k in name:
			# 			self.baseurl = "https://www.25game.com" + a.get("href")
			# 			return True
			# except:pass
			return False
		except urllib.error.HTTPError as e:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->urllib.error.HTTPError:",end="")
			print(e)
			return False
		except UnicodeDecodeError:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->UnicodeDecodeError")
			return False
		except:
			self.Accessible=False
			print("Game:"+key+"				SpiderName="+self.SpiderName+"->Remote end closed connection without response")
			return False
		finally:
			self.mutex.release()
