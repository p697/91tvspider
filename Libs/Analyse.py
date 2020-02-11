import sys
import os
sys.path.append(os.getcwd())
sys.path.append(os.path.pardir)

from Libs import Spi


def FindMax():
    maxLike = 0
    maxLikeID = ''
    for li in data:
        if int(li[2]) == 0:
            continue
        rate = int(li[1])/int(li[2])
        if rate > 1:
            print(li)
        if  rate > maxLike and rate < 0.7:
            maxLike = rate
            maxLikeID = li[0]
    print(maxLike)
    return maxLikeID


def FindByID(ID):
    for li in data:
        if li[0] == ID:
            return li
    return None

def Top100():
	singleList = []
	lists = Spi.getCSV("../数据分析/OutPut100_R.csv")
	for li in lists:
		if int(li[2]) == 0:
			li[2] = 999999
		singleList.append(int(li[1])/int(li[2]))
	maxList = []
	maxIndex = []
	for _ in range(10000):
		maxNumber = max(singleList)
		maxNumberIndex = singleList.index(maxNumber)
		maxList.append(maxNumber)
		maxIndex.append(maxNumberIndex)
		singleList[maxNumberIndex] = 0

	outp = []
	for i in maxIndex:
		ni = lists[i][:5]
		ni.append(eval(lists[i][5])[1])
		ni.append(eval(lists[i][5])[2])
		outp.append(ni)
		
	outp[888]
	outp2 = []
	for ot in outp:
		if int(ot[1]) < 500 or (int(ot[1])/int(ot[2])) > 0.8:
			continue
		outp2.append(ot)
	
	print(outp2)


def topByClass(clas):
	lists = Spi.getCSV("../数据分析/OutPut100_R.csv")
	clasList = []
	for li in lists:
		try:
			clasli = eval(li[7])
		except:
			try:
				clasli = eval(li[-8])
			except:
				clasli = []
		if clas in clasli:
			clasList.append(li)

	singleList = []
	for li in clasList:
		singleList.append(int(li[1]))

	indexList = []
	maxList = []
	for _ in range(300):
		maxNumber = max(singleList)
		maxIndex = singleList.index(maxNumber)
		maxList.append(maxNumber)
		indexList.append(maxIndex)
		singleList[maxIndex] = 0
	
	outp = []
	for i in indexList:
		ot = clasList[i][:5]
		ot.append(eval(clasList[i][5])[1])
		ot.append(eval(clasList[i][5])[2])
		outp.append(ot)
	
	print(outp)

topByClass(236)








