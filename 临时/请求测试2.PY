import requests
import json
import time
import random
import csv
import os


def ChangeProxy():
    global ipNumber
    ipNumber += 1
    res = requests.get(
        url="http://183.129.244.16:88/open?user_name=cavanotp1&timestamp=1581061809&md5=8E3F7E532A0175AE66B6A1B7DFDB3308&pattern=json&number=1")
    IP = json.loads(res.text)
    return str(IP["port"][0])


def Post(i):
    global outPut, startID, endID, successNumber, prox
    url = "http://capi.rx723.com:80/vodapi.html"

    proxies = {
        "http": "http://183.129.244.16:" + str(prox)
    }

    datas = {
        "Action": "GetMovieInfoByMember",
        "Message": {
            "MovieID": i,
            "MemberID": "2762057",
            "Token": "8A03D4DCC0294E0581DBAED55F573406"
        }
    }

    datas = json.dumps(datas)
    data = {"data": datas
            }
    try:
        res = requests.post(url=url, data=data, proxies=proxies, timeout=10)
    except Exception as e:
        print("代理失效或请求出错")
        print("Msg: " + str(e)[:30])
        prox = ChangeProxy()
        while not prox:
            time.sleep(1)
            prox = ChangeProxy()
        print("更换ip：" + prox["ip"] + ":" + str(prox["port"]))
        return False
    if(res.status_code == 200):
        tex = json.loads(res.text)
        if(tex["Result"]):
            op = []
            op.append(tex["Message"]["MovieID"])
            op.append(tex["Message"]["FavoriteCount"])
            op.append(tex["Message"]["PlayCount"])
            op.append(tex["Message"]["FileSize"])
            op.append(tex["Message"]["ChannelID"])

            images = []
            images.append(tex["Message"]["Img"])
            images.append(tex["Message"]["CoverImg"])
            images.append(tex["Message"]["CutPicName"])
            op.append(images)

            texts = []
            texts.append(tex["Message"]["Name"])
            texts.append(tex["Message"]["Description"])
            op.append(texts)

            classes = []
            for c in range(len(tex["Message"]["Class"])):
                classes.append(tex["Message"]["Class"][c]["ID"])
            op.append(classes)

            actores = []
            for a in range(len(tex["Message"]["Actor"])):
                actores.append(tex["Message"]["Actor"][a]["ID"])
            op.append(actores)

            op.append(tex["Message"]["CreateTime"])

            Save(op)
            successNumber += 1
            print("【" + str(round((startID - i)*100/(startID - endID), 4)
                            ) + "%" + "】success: " + str(i))
            # print(op)
        else:
            print("【" + str(round((startID - i)*100/(startID - endID), 4)
                            ) + "%" + "】fail: " + str(i) + "; Msg: " + str(tex["Message"]))
        return True
    else:
        print("限制：" + res.text[:50] + "...")
        prox = ChangeProxy()
        while not prox:
            time.sleep(1)
            prox = ChangeProxy()
        print("更换ip：" + prox["ip"] + ":" + str(prox["port"]))
        return False


def Save(op):
    with open('OutPut.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(op)


def Sp(stID, enID):
    global i
    for i in range(stID, enID, -1):
        while not Post(i):
            print("--------------------------")


startID = 5123325
endID = 5123000
i = startID
startID2 = startID

successNumber = 0
ipNumber = 0
startTime = time.time()
prox = ChangeProxy()


# 检测文件是否存在
csvHeads = ['MovieID', 'FavoriteCount', 'PlayCount', 'FileSize',
            'ChannelID', 'Images', 'Name/Description', 'Class', 'Actor', 'CreateTime']
if not os.path.exists('OutPut.csv'):
    with open('OutPut.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(csvHeads)
    print("文件创建成功")

while i > (endID + 1):
	try:
		Sp(startID2, endID)
	except Exception as e:
		print("异常: " + str(e))
		print("重新连接------------")
		time.sleep(1)
		i += 1
		startID2 = i + 1


endTime = time.time()
print("爬取：" + str(startID - endID))
print("有效: " + str(successNumber))
print("耗时: " + str(int(endTime - startTime)))
print("消耗IP: " + str(ipNumber))
