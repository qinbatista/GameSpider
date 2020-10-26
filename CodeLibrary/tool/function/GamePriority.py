# -*- coding: utf-8 -*-
import requests
import json
from function import settings
from bs4 import BeautifulSoup
class GPSpider:
	#Channel Param Start
	ChannelName = "GP"
	Sku = 'e2w'
	UserName = 'qin@east2west.cn'
	password = 'qinyupeng1'
	LoginPostLink = 'http://east2west.cn/dashboard/index.php/Index/Ajax/login'
	header = {
		'Host':'east2west.cn',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
		'Accept':'*/*',
		'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
		'Accept-Encoding':'gzip, deflate',
		'Referer':'http://east2west.cn/dashboard/index.php/Index/Home/login',
	}
	#Channel Param End
	def __init__(self):
		self.Session = requests.session()
		data = {
			'sku':self.Sku,
		    'account':self.UserName,
			'password':self.password,
		}
		self.Session.post(self.LoginPostLink,headers = self.header,data = data)
	def GPSpider_Revenue(self):
		url = 'http://east2west.cn/dashboard/index.php/Admin/Home/publishlist?launchstatus=&platform=Android,iOS,PC,Console,Html5&keywords=&region='
		res = self.Session.get(url,headers = self.header)
		soup = BeautifulSoup(res.text,features='html.parser')
		table = soup.find('table',{'class':'table-radius management'})
		tr_list = table.find_all('tr')
		n = 0
		self._GP_dict = {'S':[],'A':[],'B':[],'C':[],'D':[],'TBD':[]}
		for tr in tr_list:
			if n != 0:
				m = '0'
				td_list = tr.find_all('td')
				for td in td_list:
					if m == '0':
						m = td.text
					elif m != '0' and m != '1':
						if m != '' and td.text != '' and td.text not in self._GP_dict['S']:
							if td.text not in self._GP_dict['A']:
								if td.text not in self._GP_dict['B']:
									if td.text not in self._GP_dict['C']:
										if td.text not in self._GP_dict['D']:
											if td.text not in self._GP_dict['TBD']:
												self._GP_dict[m].append(td.text)
						m = '1'
			n = n+1
		print(self._GP_dict)
	def SaveContext(self):
		with open(settings.e2wGamePath + "/Cache/"+self.ChannelName+".json", 'w',encoding='utf-8') as out:
			json.dump(self._GP_dict, out, ensure_ascii=False)
def main():
	GP = GPSpider()
	GP.GPSpider_Revenue()
	GP.SaveContext()
if __name__ == '__main__':
	main()
