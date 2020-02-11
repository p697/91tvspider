import sys
import os
sys.path.append(os.getcwd())

from Libs import Spi

def findSmallest(number,max=50000):
    lists = Spi.getCSV("OutPut100_R临时.csv")

    sizeList = []
    for li in lists[:max]:
        if(int(li[3]) < 10000000):
            sizeList.append(9999999999)
        else:
            sizeList.append(int(li[3]))


    minSizeList = []
    minSizeIndex = []
    for _ in range(number):
        minSize = min(sizeList)
        minSizeList.append(minSize)
        minIndex = sizeList.index(minSize)
        minSizeIndex.append(minIndex)
        sizeList[minIndex] = 9999999999
    
    return minSizeIndex

    



