import xlwt
import os
import json
import chardet
import sys
from xlrd import open_workbook
from xlutils.copy import copy
#This is the class to export particular json format to particular excel format, the limit of raw is 65532， the limit of line is 255
class QinExcelClass:
	def __init__(self):
		self.GameNameList = []
		self.WebNameList = []
		self.LinkList = []
	def AnalysisData(self,ExcelLocation,JsonLocation):
		#create new excel
		book = xlwt.Workbook(encoding='utf-8',style_compression=0)
		book.add_sheet('OnlineSituation',cell_overwrite_ok=True)
		book.save(ExcelLocation)
		self.AnalysisJson(JsonLocation)
		#write to excel
		for i in range(len(self.GameNameList)):
			self.WriteToExcel(ExcelLocation,0,i+1,self.GameNameList[i])
		ChannelCount = int(len(self.WebNameList)/len(self.GameNameList))
		for webcount in range(ChannelCount):
			self.WriteToExcel(ExcelLocation,webcount+1,0,self.WebNameList[webcount])
		for Y in range(len(self.GameNameList)):
			for webcount in range(int(len(self.WebNameList)/len(self.GameNameList))):
				if self.LinkList[webcount+Y*int(len(self.WebNameList)/len(self.GameNameList))]=="":
					self.WriteToExcel(ExcelLocation,webcount+1,Y+1,"x")
				elif self.LinkList[webcount+Y*int(len(self.WebNameList)/len(self.GameNameList))]=="-":
					self.WriteToExcel(ExcelLocation,webcount+1,Y+1,"-")
				else:
					self.WriteToExcel(ExcelLocation,webcount+1,Y+1,"√")
				print(str(webcount+1)+" "+str(Y))
	def GetEncoding(self,_Path):
		myfile = open(_Path,'rb')
		data = myfile.read()
		di= chardet.detect(data)
		myfile.close()
		myencoding = di["encoding"]
		if myencoding==None:
			myencoding ="utf-8"
		return myencoding
	#This method can't write raw over 256
	def WriteToExcel(self,ExcelLocation,x,y,text):
		rb = open_workbook(ExcelLocation)
		wb = copy(rb)
		rb.sheet_by_index(0)
		ws = wb.get_sheet(0)
		ws.write(y, x, text)
		wb.save(ExcelLocation)
	def AnalysisJson(self,JsonLocation):
		readed = json.load(open(JsonLocation, 'r',encoding=self.GetEncoding(JsonLocation)))
		for GameName in readed :
			self.GameNameList.append(GameName)
		self.GameNameList.sort(reverse=True)
		for Game in self.GameNameList:
			for str in range(len(readed[Game])):
				if str%2==0:
					self.WebNameList.append(readed[Game][str])
					self.LinkList.append(readed[Game][str+1])


if __name__=='__main__':
	test = QinExcelClass()
	test.AnalysisData(sys.path[0]+"/GamePublishList.xls",sys.path[0]+"/results.json")
