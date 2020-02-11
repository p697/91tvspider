import csv
import requests
import numba
import sys
import os
sys.path.append(os.getcwd())

from Libs import GetVideo
from Libs import Spi



def Test(ID):
    m3u8Result = GetVideo.getVideoM3u8(ID)
    if m3u8Result["Result"]:
        res = requests.get(url = m3u8Result["Message"])
        if res.status_code == 200:
            print(str(ID) + " --- " + str(res.status_code))
            return True
        else:
            print(str(ID) + " --- " + str(res.status_code))
            return False
    else:
        print(str(ID) + " --- None --- " + m3u8Result["Message"])
        return False

        
with open("数据分析/OutPut100.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    result = list(reader)
    lists = result[1:]


def Circle():
    IDlist = []
    for li in lists:
        IDlist.append(li[0])

    for li in range(len(lists)):
        lis = lists[li]
        if len(lis) > 10:
                lis = lis[:10]
        if Test(lis[0]):
            lis.append(True)
        else :
            lis.append(False)
        lists[li] = lis

Circle()

with open('OutPut_Test.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(lists)
    
    


    




