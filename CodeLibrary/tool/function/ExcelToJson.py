# -*- coding: utf-8 -*-
import xlrd,xlwt,os,json
def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))
class ExcelToJson():
	JsonDict = {}
	SABCD = ['S','A','B','C','D','TBD']
	def AnalysisExcel(self, ExcelLocation, JsonLocation):
		book = xlrd.open_workbook(ExcelLocation,formatting_info=True)
		rb = book.sheet_by_index(1)
		key = ''
		Game = []
		maxn = 0
		for row in range(rb.nrows):
			if key != '' and key != rb.cell(row, 0).value:
				self.JsonDict.update({key:Game})
				Game = []
			key = rb.cell(row, 0).value
			coln = 0
			for col in range(rb.ncols):
				if coln > 0:
					Game.append(rb.cell(row, col).value)
					if len(Game) > maxn:
						maxn = len(Game)
				coln = coln + 1
		Game = []
		for n in range(maxn):
			Game.append('15-')
		for sab in self.SABCD:
			self.JsonDict.update({sab:Game})
		self.SaveJson(JsonLocation)
	def SaveJson(self,JsonLocation):
		if os.path.exists(PythonLocation()+"/../cache")==False:
			os.mkdir(PythonLocation()+"/../cache")
		with open(JsonLocation, 'w',encoding='utf-8') as out:
			json.dump(self.JsonDict, out, ensure_ascii=False)#ensure_ascii=False 以中文形式输入
def main():
	xls = ExcelToJson()
	xls.AnalysisExcel(PythonLocation() + '/../GamePublishList.xls',PythonLocation() + '/../cache/results.json')
if __name__ == '__main__':
	main()