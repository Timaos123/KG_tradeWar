#coding:utf8

import requests
from urllib.request import quote

if __name__=="__main__":
    keywords=quote("trade war electronic")
    # first d8v1
    headers={
        "Host": "mab.chartbeat.com",
        "Connection": "keep-alive",
        "Origin": "https://www.scmp.com",
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
        "Accept": "*/*",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Referer": "https://www.scmp.com/content/search/{}".format(keywords),
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    params={
        "host":"scmp.com",
        "domain":"scmp.com",
        "path":"%2Fcontent%2Fsearch%2Ftrade%2520war%2520electronic"
    }
    mainPage=requests.get("https://mab.chartbeat.com/mab_strategy/headline_testing/get_strategy/",
                            params=params,
                            headers=headers)
    with open("mabreturn.json","w+",encoding="utf8") as mainPageFile:
        mainPageFile.write(mainPage.text)