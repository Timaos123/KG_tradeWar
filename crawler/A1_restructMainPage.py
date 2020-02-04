#coding:utf8

import json
import pandas as pd
import numpy as np
import os
import tqdm

def json2Df(jsonFileName):
    with open(jsonFileName,"r",encoding="utf8") as myJsonFile:

        myJson=json.load(myJsonFile)
        
        newList=[]
        originList=myJson[0]["data"]["searchElasticsearchQuery"]["results"]

        #find title, url and uid
        for originItem in originList:

            titleItem=originItem["entityLabel"]
            urlItem="https://www.scmp.com"+originItem["entityUrl"]["path"]
            uidItem=originItem["entityUuid"]

            newList.append([titleItem,urlItem,uidItem])
        
    return pd.DataFrame(np.array(newList).reshape(-1,3),columns=["title","url","uid"])

if __name__=="__main__":
    i=int(input("1:restart,0:resume"))
    for fileName in tqdm.tqdm(os.listdir("data/mainPageJSON")):
        if fileName.endswith(".json"):
            # integrate all json files into csv
            newDf=json2Df("data/mainPageJSON/"+fileName)
            if i==1:
                newDf.to_csv("data/rawData.csv",index=None)
                i=0
            else:
                newDf.to_csv("data/rawData.csv",index=None,header=None,mode="a")