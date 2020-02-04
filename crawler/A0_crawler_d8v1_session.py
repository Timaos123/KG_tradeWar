#coding:utf8

import requests
from urllib.request import quote
import json
import time
import tqdm
import numpy as np
import os
from tryEmail import sendEmail

def main(keyWords,startPage=0,totalPage=517):
    keywords=quote(keyWords)
    # first d8v1
    headers1={
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
    headers2={
        "Host": "apigw.scmp.com",
        "Connection": "keep-alive",
        "Content-Length": "1813",
        "accept": "*/*",
        "Origin": "https://www.scmp.com",
        "apikey": "MyYvyg8M9RTaevVlcIRhN5yRIqqVssNY",
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
        "content-type": "application/json;charset=UTF-8",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Referer": "https://www.scmp.com/content/search/{}".format(keywords),
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    Json=[{"operationName":"SearchElastic",
            "variables":{
                "keyword":"trade war electronic",
                "applicationId":"325477",
                "page":0,
                "pageSize":20},
            "query":"query SearchElastic($keyword: String!, $pageSize: Int!, $page: Int!, $applicationId: String!) {\n  searchElasticsearchQuery(filter: {search: $keyword, app_id: $applicationId}, pageSize: $pageSize, page: $page) {\n    count\n    results {\n      entityUuid\n      entityId\n      entityLabel\n      entityBundle\n      entityUrl {\n        path\n        __typename\n      }\n      ... on NodeArticle {\n        body {\n          summary\n          __typename\n        }\n        fieldImages {\n          url\n          title\n          size_118X118: derivative(style: _118X118) {\n            url\n            __typename\n          }\n          __typename\n        }\n        fieldSection {\n          entity {\n            name\n            __typename\n          }\n          __typename\n        }\n        fieldPublishedDate\n        __typename\n      }\n      ... on NodeVideo {\n        body {\n          summary\n          __typename\n        }\n        fieldImages {\n          url\n          title\n          size_118X118: derivative(style: _118X118) {\n            url\n            __typename\n          }\n          __typename\n        }\n        fieldVideoSection {\n          entity {\n            name\n            __typename\n          }\n          __typename\n        }\n        fieldPublishedDate\n        __typename\n      }\n      ... on NodeGallery {\n        fieldImages {\n          url\n          title\n          size_118X118: derivative(style: _118X118) {\n            url\n            __typename\n          }\n          __typename\n        }\n        fieldPublishedDate\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
            }]

    for i in range(startPage,totalPage):
        print(i+1,"/",totalPage)
        #build a new session
        mySession=requests.session()
        requests.chardet="utf8"
        Json[0]["variables"]["page"]=i
        mySession.options("https://apigw.scmp.com/d8/v1",headers=headers1,verify=False)
        mainPage=mySession.post("https://apigw.scmp.com/d8/v1",headers=headers2,json=Json)

        #get json posted
        d8v1Json=json.loads(mainPage.text)

        if "mainPageJSON" not in os.listdir("data"):
            os.mkdir("data/mainPageJSON")

        # save json
        with open("data/mainPageJSON/d8v1_{}.json".format(i),"w+",encoding="utf8") as d8v1JsonFile:
            json.dump(d8v1Json,d8v1JsonFile)
        
        sleepTime=np.random.random()*10+5
        print("sleeping {}s...".format(sleepTime))
        time.sleep(sleepTime)

if __name__=="__main__":
    try:
        main("trade war electronic",0,200)
    except Exception as ex:
        # send message about the error with e-mail, if error arises
        sendEmail(str(ex))