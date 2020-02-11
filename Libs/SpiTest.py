import json
import sys
import os
sys.path.append(os.getcwd())

from Libs import Spi



data = {
    "data": json.dumps({
    "Action": "PlayMovie2",
    "Message": {
        "MovieID": 5120000,
        "MemberID": "2762057",
        "Type": 1,
        "Token": "DD49E9F1054F4E2EA1A790D0B9840722"
        }
    })
}


obj = {
    "url": "http://capi.rx723.com:80/vodapi.html",
    "data": data,
    "method": "post"
}
res = Spi.Spi(obj)
print(res)
