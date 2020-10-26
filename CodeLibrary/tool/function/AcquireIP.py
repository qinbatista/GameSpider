# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
def get_ip_list():
	headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36' }
	web_data = requests.get('http://www.xicidaili.com/nn/', headers=headers)
	soup = BeautifulSoup(web_data.text, 'html.parser')
	ips = soup.find_all('tr')
	ip_list = []
	for i in range(1, len(ips)):
		ip_info = ips[i]
		tds = ip_info.find_all('td')
		if tds[5].text == 'HTTP':
			dc = {}
			dc.update({'http':'http://' + tds[1].text + ':' + tds[2].text})
			ip_list.append(dc)
	print("获取西刺代理IP")
	return ip_list
if __name__ == '__main__':
	ip_list = get_ip_list()
	print(ip_list)
	# for ip in ip_list:
	# 	print(ip)