
import requests
import json
import os
import csv
import psutil
import sys
import time
import urllib.request
sys.path.append(os.getcwd())
sys.path.append(os.path.pardir)
from Libs import Spi
from Libs import FindSmallest


# 通过ID获取视频m3u8ziyuan
def getVideoM3u8(ID):
    url = "http://capi.rx723.com:80/vodapi.html"
    datas = {
        "Action": "PlayMovie2",
        "Message": {
            "MovieID": ID,
            "MemberID": "2762057",
            "Type": 1,
            "Token": "DD49E9F1054F4E2EA1A790D0B9840722"
        }
    }
    datas = json.dumps(datas)
    data = {
        "data": datas
    }

    res = requests.post(url=url, data=data)
    result = json.loads(res.text)
    return result


# 下载单个视频
def downloadVideo(ID):    
    isExist = os.path.exists('F:/毛概ppt/2019214008/' + ID + "/" + ID + ".mp4")
    isExist2 = os.path.exists('F:/毛概ppt/2019214008/' + ID + "-/" + ID + ".mp4") 
    if isExist or isExist2:
        print("exists --- " + ID + ".mp4")
        return False
    result = getVideoM3u8(ID)
    if result["Result"] == 1:
        m3u8 = result["Message"]
        cmd = 'ffmpeg  -i "' + m3u8 + \
            '" -vcodec copy -acodec copy -absf aac_adtstoasc  F:/毛概ppt/2019214008/' + ID + "/" +\
            ID + '.mp4 '
        d = os.popen(cmd)
        if d == 0:
            return True
    else:
        return False


# 下载单个图片
def downloadImage(dirc, ID):
	li = getInfoByID(ID)
	imgUrl = eval(li[5])[1]
    # urlretrieve不好用
    # opener = urllib.request.build_opener()
    # opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36')]
    # urllib.request.install_opener(opener)
    # urllib.request.urlretrieve(imgUrl, filename=('F:/毛概ppt/2019214008/' + ID + "/" + ID + ".jpg"))
	req = urllib.request.Request(imgUrl)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36')
	req.add_header('Cache-Control', 'no-cache')
	req.add_header('Accept', '*/*')
	req.add_header('Accept-Encoding', 'gzip, deflate')
	req.add_header('Connection', 'Keep-Alive')
	
	resp = urllib.request.urlopen(req)
	respHtml = resp.read()

	binfile = open(dirc, "wb")
	binfile.write(respHtml)

	binfile.close()
	print("finish --- " + str(ID))
	return True


# 通过ID索引详细信息
def getInfoByID(ID):
    lists = Spi.getCSV("数据分析/OutPut100_R.csv")
    if isinstance(ID, list):
        outPut = []
        for li in lists:
            for Id in ID:
                if str(li[0]) == str(Id):
                    outPut.append(li)
                    print(Id)
                    break
        return outPut

    for li in lists:
        if str(li[0]) == str(ID):
            return li
    return None


# 获取我的收藏视频IDs
def getMyFavorite():
    url = "http://capi.rx723.com:80/vodapi.html"
    datas = {
        "Action": "GetMyFavorite2",
        "Message": {
            "PageIndex": 1,
            "MemberID": "2762057",
            "Token": "DD49E9F1054F4E2EA1A790D0B9840722",
            "PageSize": 200
        }
    }
    datas = json.dumps(datas)
    data = {
        "data": datas
    }

    res = requests.post(url=url, data=data)
    result = json.loads(res.text)
    lists = result["Message"]["Data"]
    IDLists = []
    for li in lists:
        IDLists.append(li["MovieID"])
    # 暂时注释掉，计算视频文件总大小
    # size = 0
    # aLists = getInfoByID(IDLists)
    # for li in aLists:
    #     size += int(li[3])
    # print("size: " + str(size/1000000) + "Gb")
    return IDLists


# 获取当前ffmpeg进程数
def getFFmpegProc():
    ffmpeg = 0
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name'])
        except psutil.NoSuchProcess:
            pass
        else:
            ffmpeg = ffmpeg + 1 if pinfo["name"] == "ffmpeg.exe" else ffmpeg
    return ffmpeg


# 通过索引获取id
def getID_byIndex(indexes):
    lists = Spi.getCSV("数据分析/OutPut100_R.csv")
    IDs = []
    for i in indexes:
        IDs.append(lists[i][0])
    return IDs


# 批量下载
def DownloadManty(IDs, IDindex):
	ID = IDs[IDindex]
	if getFFmpegProc() < 10:
		print("进程接入: --------" + str(ID))
		time.sleep(0.2)
		downloadVideo(ID)
	else:
		while True:
			time.sleep(0.2)
			if getFFmpegProc() < 10:
				break
	IDindex += 1
	if IDindex == len(IDs):
		return True
	DownloadManty(IDs, IDindex)
	

# 为批量下载做准备	
def downloadImage_R(dirc, ids):
    for ID in ids:
        isExist = os.path.exists(dirc + ID  + '-')
        isExist2 = os.path.exists(dirc + ID)
        isExist3 = os.path.exists(dirc + ID  + '-/' + ID + '.jpg')
        isExist4 = os.path.exists(dirc + ID + '/' + ID + '.jpg')
        if not isExist and not isExist2:
            os.makedirs(dirc + ID)
            downloadImage(dirc + ID + '/' + ID + '.jpg', ID)
        else:
            if isExist and not isExist3:
                downloadImage(dirc + ID  + '-/' + ID + '.jpg', ID)
            elif isExist2 and not isExist4:
                downloadImage(dirc + ID  + '/' + ID + '.jpg', ID)
            else:
                print("existImg --- " + str(ID))


# DownloadManty(getMyFavorite(), 0)
        
# print(getInfoByID(5062591))
    
# downloadImage_R('F:/毛概ppt/2019214008/', getMyFavorite())
    
