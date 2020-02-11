import requests
import json
import time
import random
import csv
import os


def getCSV(name):
    with open(name, encoding="utf-8") as f:
        reader = csv.reader(f)
        result = list(reader)
        lists = result[1:]
    return lists


def Post(i):
    global outPut, startID, endID, successNumber, prox
    url = "http://capi.rx723.com:80/vodapi.html"

    proxies = {
        "http": "http://" + prox["ip"] + ":" + str(prox["port"])
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





def GetProxy(proxyApi):
    res = requests.get(url=proxyApi)
    if res.status_code != 200 or not res.text:
        print("代理api出错，尝试重连")
        print("------------------")
        time.sleep(1)
        GetProxy(proxyApi)
    IP = json.loads(res.text)
    if not IP["data"]:
        print("代理api出错，尝试重连")
        print("------------------")
        time.sleep(1)
        GetProxy(proxyApi)
    print("更换代理: " + str(IP))
    print("------------------")
    proxies = {
        "http": "http://" + IP["ip"] + ":" + str(IP["port"])
    }    
    return proxies

def SpiGet(url, headers):
    res = requests.get(url=url, headers=headers)
    if res.status_code != 200 or not res.text:
        return False
    return json.loads(res.text)

def SpiPost(url, headers, data):
    res = requests.post(url=url, headers=headers, data=data)
    if res.status_code != 200 or not res.text:
        return False
    return json.loads(res.text)

def SpiGetProxy(url, headers, proxies):
    res = requests.get(url=url, headers=headers, proxies=proxies)
    if res.status_code != 200:
        return False
    return json.loads(res.text)

def SpiPostProxy(url, headers, data, proxies):
    res = requests.post(url=url, headers=headers, data=data, proxies=proxies)
    if res.status_code != 200:
        return False
    return json.loads(res.text)



# 检测文件是否存在
# obj:{
#     url: must
#     method: post/get must
#     headers: choose
#     data: choose
#     proxies: choose
# }
def Spi(obj):
    url = obj["url"]
    method = obj["method"]
    if method != "get" and method != "post":
        return "method wrong" 
    headers = obj["headers"] if "headers" in obj.keys() else None
    data = obj["data"] if "data" in obj.keys() else None
    proxyStatu = True if "proxies" in obj.keys() else False
    proxies = obj["proxies"] if proxyStatu else None

    if not proxyStatu and method == "get":
        return SpiGet(url, headers)
    elif not proxyStatu and method == "post":
        return SpiPost(url, headers, data)
    elif proxyStatu and method == "get":
        return SpiGetProxy(url, headers, proxies)
    else:
        return SpiPostProxy(url, headers, data, proxies)
        
        
         



