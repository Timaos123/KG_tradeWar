#coding:utf8

import requests
from urllib.request import quote

if __name__=="__main__":
    keywords=quote("trade war electronic")
    # first d8v1
    headers={
        "Host": "apigw.scmp.com",
        "Connection": "keep-alive",
        "Access-Control-Request-Method": "POST",
        "Origin": "https://www.scmp.com",
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
        "Access-Control-Request-Headers": "apikey,content-type",
        "Accept": "*/*",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Referer": "https://www.scmp.com/content/search/{}".format(keywords),
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    # second d8v1
    # headers={
    #     "Host": "apigw.scmp.com",
    #     "Connection": "keep-alive",
    #     "Content-Length": "1813",
    #     "accept": "*/*",
    #     "Origin": "https://www.scmp.com",
    #     "apikey": "MyYvyg8M9RTaevVlcIRhN5yRIqqVssNY",
    #     "User-Agent": "Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
    #     "content-type": "application/json",
    #     "Sec-Fetch-Site": "same-site",
    #     "Sec-Fetch-Mode": "cors",
    #     "Referer": "https://www.scmp.com/content/search/{}".format(keywords),
    #     "Accept-Encoding": "gzip, deflate, br",
    #     "Accept-Language": "zh-CN,zh;q=0.9",
    # }
    mainPage=requests.options("https://apigw.scmp.com/d8/v1",headers=headers)
    with open("wtf.html","w+",encoding="utf8") as mainPageFile:
        mainPageFile.write(mainPage.text)