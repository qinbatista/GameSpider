# -*- coding: utf-8 -*-
import os
import json
import chardet
import time
import xlsxwriter
# import xlwings
from function import settings


def PythonLocation():
	return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


# This is the class to export particular json format to particular excel format, the limit of raw is 65532， the limit
#  of line is 255 ValueError: column index (256) not an int in range(256)
class QinExcelClass:
	def __init__(self):
		self.SABCD = ["S", "A", "B", "C", "D", "TBD"]
		self.SituationList = []
		self.SituationListWeb = []

	def AnalysisData(self, ExcelLocation, JsonLocation):
		self.AnalysisJson(JsonLocation)
		# write to excel
		print("写入Excel文件内容中......")
		self.WriteToExcel(ExcelLocation, 0, len(self.SituationList[0]), 0, len(self.SituationList), 0, len(self.SituationListWeb[0]), 0, len(self.SituationListWeb))
		# self.ReadExcel(ExcelLocation)
		print("Excel文件内容写入结束！")

	def GetEncoding(self, _Path):
		myfile = open(_Path, 'rb')
		data = myfile.read()
		di = chardet.detect(data)
		myfile.close()
		myencoding = di["encoding"]
		if myencoding is None:
			myencoding = "utf-8"
		return myencoding

	def WriteToExcel(self, ExcelLocation, x0, x1, y0, y1, x10, x11, y10, y11):
		workbook = xlsxwriter.Workbook(ExcelLocation)  # 创建一个excel文件
		worksheet0 = workbook.add_worksheet(name="OnlineSituation")
		worksheet1 = workbook.add_worksheet(name="OnlineSituationWeb")
		for y in range(y1 - y0):
			if self.SituationList[y + y0][0] in self.SABCD:
				style = workbook.add_format({'border': 1, 'bg_color': 'yellow', 'align': 'center'})
			else:
				style = workbook.add_format({'border': 1, 'align': 'center'})
			for x in range(x1 - x0):
				if x + x0 != 0 and y + y0 != 0 and self.SituationList[y + y0][x + x0] == "":
					worksheet0.write(y + y0, x + x0, "✖", style)
				elif "http" in self.SituationList[y + y0][x + x0]:
					worksheet0.write(y + y0, x + x0, "✔", style)
				elif self.SituationList[y + y0][x + x0] == '15-':
					worksheet0.write(y + y0, x + x0, self.SituationList[y + y0][0], style)
				elif self.SituationList[y + y0][x + x0] == '-':
					worksheet0.write(y + y0, x + x0, self.SituationList[y + y0][x + x0], style)
				else:
					worksheet0.write(y + y0, x + x0, self.SituationList[y + y0][x + x0], style)
		for y in range(y11 - y10):
			for x in range(x11 - x10):
				if self.SituationListWeb[y + y10][x + x10] == '15-' or self.SituationListWeb[y + y10][
					x + x10] in self.SABCD:
					worksheet1.write(y + y10, x + x10, self.SituationListWeb[y + y10][0], workbook.add_format({'border': 1, 'bg_color': 'yellow', 'align': 'center'}))
				else:
					worksheet1.write(y + y10, x + x10, "" if self.SituationListWeb[y + y10][x + x10] == "-" else
					self.SituationListWeb[y + y10][x + x10])
		workbook.close()

	"""读取Excel文件的方法"""  # 暂时无用
	"""
	def ReadExcel(self, ExcelLocation):
		app = xlwings.App(visible=False, add_book=False)
		wb = app.books.open(ExcelLocation)
		# 引用某指定sheet
		sheet = wb.sheets[0]
		print("Time:", time.strftime("%H:%M:%S", time.localtime(time.time())), sep="")
		nrow = 0  # 行
		while sheet[nrow, 1].value != None:
			nrow = nrow + 1
		ncol = 0  # 列
		while sheet[1, ncol].value != None:
			ncol = ncol + 1
		print(nrow, ncol)
		print("Time:", time.strftime("%H:%M:%S", time.localtime(time.time())), sep="")
		wb.save(PythonLocation() + "/cache/GamePublishList_log.xlsx")
		wb.close()
		app.quit()
	"""

	def AnalysisJson(self, JsonLocation):
		readed = json.load(open(JsonLocation, 'r', encoding=self.GetEncoding(JsonLocation)))
		Game_Rows = []  # 筛选出第一列的游戏标题
		for GameName in readed:
			Game_Rows.append(GameName)
		Game_Cols = [""]  # 筛选出第一行的渠道标题
		for Game in Game_Rows:
			if Game != "":
				for value in range(len(readed[Game])):
					if value % 2 == 0 and readed[Game][value] and readed[Game][value] != "15-":
						Game_Cols.append(readed[Game][value])
				if "15-" in Game_Cols:
					Game_Cols = [""]
				elif len(Game_Cols) != 1:
					break
		self.SituationList.append(Game_Cols)
		"""#self.Rows为行数，0为第一行；self.Cols为列数，0为第一列
		self.Rows = len(Game_Rows)
		self.Cols = len(Game_Cols)
		"""
		for Game in Game_Rows:
			Game_Cols = [Game]
			for str in range(len(readed[Game])):
				if str % 2 == 0:
					Game_Cols.append(readed[Game][str + 1])
			self.SituationList.append(Game_Cols)
		SABCD = []
		Game_Cols = []
		for Game in Game_Rows:
			for str in range(len(readed[Game])):
				if str % 2 == 0:
					if Game not in self.SABCD or Game not in SABCD:
						if Game in self.SABCD:
							SABCD.append(Game)
						Game_Cols.append(Game)
						Game_Cols.append(readed[Game][str])
						Game_Cols.append(readed[Game][str + 1])
						self.SituationListWeb.append(Game_Cols)
						Game_Cols = []


if __name__ == '__main__':
	print("Time:", time.strftime("%H:%M:%S", time.localtime(time.time())), sep="")
	test = QinExcelClass()
	test.AnalysisData(settings.e2wGamePath + "/AppMonitor/" + settings.mkPath + "/GamePublishList.xlsx",
	                  settings.e2wGamePath + "/AppMonitor/" + settings.mkPath + "/results.json")
	print("Time:", time.strftime("%H:%M:%S", time.localtime(time.time())), sep="")
# test.AnalysisJson(settings.e2wGamePath + "/AppMonitor/" + settings.mkPath + "/results.json")
# test.AnalysisJson(settings.e2wGamePath + "/AppMonitor/" + settings.mkPath + "/results_log.json")
