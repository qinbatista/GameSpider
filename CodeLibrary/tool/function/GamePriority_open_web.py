# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time
from function import settings
import json
from bs4 import BeautifulSoup
class GPSpider:
	#Channel Param Start
	ChannelName = "GP"
	Sku = 'e2w'
	UserName = 'qin@east2west.cn'
	password = 'qinyupeng1'
	LoginPostLink = 'http://east2west.cn/dashboard/index.php/Index/Home/login'
	#Channel Param End
	def __init__(self):
		self.driver=webdriver.Firefox()
		self.driver.get(self.LoginPostLink)
		wait=WebDriverWait(self.driver,10)
		self.driver.find_element_by_id('sku').send_keys(self.Sku)
		self.driver.find_element_by_id('account').send_keys(self.UserName)
		self.driver.find_element_by_id('password').send_keys(self.password)
		time.sleep(0.5)
		self.driver.find_element_by_id('login_btn').click()
		print("登陆成功")
		time.sleep(0.5)
	def GPSpider_Revenue(self):
		self.driver.get('http://east2west.cn/dashboard/index.php/Admin/Home/publishlist?launchstatus=&platform=Android,iOS,PC,Console,Html5&keywords=&region=')
		soup = BeautifulSoup(self.driver.page_source,features='html.parser')
		table = soup.find('table',{'class':'table-radius management'})
		tbody = table.find('tbody')
		tr_list = tbody.find_all('tr')
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
		time.sleep(0.5)
		# self.strs = re.search("<([\s\S]*)>",self.driver.page_source).group()
		# print(self.strs)
		self.driver.close()
	def SaveContext(self):
		with open(settings.e2wGamePath + "/Cache/"+self.ChannelName+".json", 'w',encoding='utf-8') as out:
			json.dump(self._GP_dict, out, ensure_ascii=False)
def main():
	GP = GPSpider()
	GP.GPSpider_Revenue()
	GP.SaveContext()
if __name__ == '__main__':
	main()
