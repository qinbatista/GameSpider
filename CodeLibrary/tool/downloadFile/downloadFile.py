# downloadFile.py
#
#
# downloadFile is a program that downloads the contents of a url
# from the web and saves it to the specified file. This is useful
# for viewing the response from a website.

import urllib.request
import urllib.error
import os
import sys
def prompt_user() -> None:
	url = request_url()
	if len(url) == 0:
		return
	else:
		print()
		save_path = request_save_path()
		if len(save_path) == 0:
			return
		else:
			download_url(url, save_path)

def request_url() -> str:
	print('Choose a URL to download (press Return to quit)')
	return input('URL: ').strip()

def request_save_path() -> str:
	if os.path.exists(sys.path[0]+"/"+"DownloadFile.txt"):
		os.remove(sys.path[0]+"/"+"DownloadFile.txt")
	return (sys.path[0]+"/"+"DownloadFile.txt").strip()

def download_url(url: str, save_path: str) -> None:
	response = None
	savefile = None
	try:
		response = urllib.request.urlopen(url)
		savefile = open(save_path, 'wb')
		savefile.write(response.read())
	except urllib.error.HTTPError as e:
		print('Failed to download contents of URL')
		print('Status code: {}'.format(e.code))
		print()
	finally:
		if savefile != None:
			savefile.close()
		if response != None:
			response.close()

if __name__=='__main__':
	prompt_user()
