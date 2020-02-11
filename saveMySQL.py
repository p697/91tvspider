import pymysql
import csv
import time


def getCSV(name):
    with open(name, encoding="utf-8") as f:
        reader = csv.reader(f)
        result = list(reader)
        lists = result[1:]
    return lists

def process():
    lists = getCSV("数据分析/OutPut100_R.csv")
    datas = []
    for li in lists:
        li2 = li[0:5]
        li2.append("")
        li2.append("")
        li2.append(li[7])
        li2.append(li[8])
        li2.append(li[9])
        li2 = tuple(li2)
        datas.append(li2)
    return datas


def save(datas):
    conn = pymysql.connect(
        host="rm-bp1xh78n7jgm1kks3io.mysql.rds.aliyuncs.com",
        user="p697",
        password="13991986996@@Ab",
        database="91tv",
        charset="utf8"
    )
    cursor = conn.cursor()

    sql = 'insert into moviedata(MovieID,FavoriteCount,PlayCount,FileSize,ChannelID,Name,Description,Class,Actor,CreateTime) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'

    cursor.executemany(sql, datas)

    conn.commit()
    cursor.close()
    conn.close()
    return True


def deleRepeat():
    lists = getCSV("数据分析/OutPut100.csv")
    print("去重前长度：" + str(len(lists)))
    IDs = []
    for i in range(len(lists)-1, -1, -1):
        ID = lists[i][0]
        if ID not in IDs:
            IDs.append(ID)
        else:
            print("find --- " + str(ID))
            lists.pop(i)
    print("去重后长度: " + str(len(lists)))

    with open("数据分析/OutPut100_R.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(lists)
    return True




time1 = time.time()

if save(process()):
    print("Finish")




time2 = time.time()

print(time2 - time1)
