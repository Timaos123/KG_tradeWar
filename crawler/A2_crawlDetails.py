#coding:utf8

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import json
import time
import tqdm
import warnings
from tryEmail import sendEmail

warnings.filterwarnings('ignore')
def crawlDetails(detailPageUrl,entityUuid):
    detailPage=requests.get(detailPageUrl,verify=False)
    
    detailSoup=BeautifulSoup(detailPage.text,features="lxml")
    reportPattern=re.compile("window.__APOLLO_STATE__.*")

    try:
        reportScript=detailSoup.find_all("script",text=reportPattern)[0].contents[0].replace("window.__APOLLO_STATE__=","")

        reportDict=json.loads(reportScript)

        detailOriginJson=reportDict["contentService"]['$ROOT_QUERY.content({"contentType":"Article","filter":{"entityUuid":"'+str(entityUuid)+'","applicationId":"2695b2c9-96ef-4fe4-96f8-ba20d0a020b3"}})']
        keyWordListJson=detailOriginJson["keywords"]["json"]
    except IndexError as ex:
        return "None","None","None"

    #detail information including key words, articles and pulished date
    if len(keyWordListJson)>0:
        keyWordList=keyWordListJson[0].split(",")
    else:
        keyWordList=[]

    for keyItem in detailOriginJson.keys():
        if keyItem.startswith("body"):
            articleList=detailOriginJson[keyItem]["json"]
            break
    paragraphList=[]
    for paraComItem in articleList:
        paragraph=" ".join([pchild["data"] 
                            for pchild in paraComItem.get("children","") if pchild["type"]=="text"])
        paragraphList.append(paragraph)
    if len(paragraphList)>0:
        article=" ".join(paragraphList)
    else:
        article="None"
    
    timeStamp=detailOriginJson["publishedDate"]
    try:
        timArr=time.localtime(timeStamp/1000)
        timeStr=time.strftime("%Y-%m-%d %H:%M:%S", timArr).split(" ")[0]
    except Exception:
        timeStr="None"

    return timeStr,article,keyWordList

if __name__=="__main__":
    try:
        #load csv
        originalList=pd.read_csv("data/rawData.csv")[:2000].values.tolist()

        #scrawl the details of the news
        i=int(input("1:restart,0:resume"))
        for originalI in range(len(originalList)):
            print(originalI,"/",len(originalList))
            originalList[originalI]+=crawlDetails(originalList[originalI][1],originalList[originalI][2])

            originalItemArr=np.array([originalList[originalI]])
            originalDf=pd.DataFrame(originalItemArr,\
                                    columns=["title","url","uid","time","article","keywords"])
            if i==1:
                originalDf.to_csv("data/originalData.csv",sep="|",index=None)
                i=0
            else:
                originalDf.to_csv("data/originalData.csv",sep="|",index=None,mode="a",header=None)
            
            sleeptime=np.random.random()*5+5
            print("sleeping {}s ...".format(sleeptime))
            time.sleep(sleeptime)

    except Exception as ex:
        #send message when encountering errors
        sendEmail(str(ex))

