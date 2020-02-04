# coding:utf8

import numpy as np
import pandas as pd
import pickle as pkl
import pymysql
from sqlalchemy import create_engine
import tqdm

if __name__=="__main__":

    mySQLConnect=pymysql.connect(host="39.107.92.174", user="my7012", password="my7012", db="my7012", port=3306)
    cursor = mySQLConnect.cursor()

    with open("data/cvDict.pkl","rb") as cvDictFile:
        cvDict=pkl.load(cvDictFile)
    # print(cvDict)
    # print("================")

    nvnDf=pd.read_csv("data/newNvnDf.csv").loc[:50]
    ####################################################################
    vnsoDict={}
    for row in nvnDf.values.tolist():
        vnsoDict[row[2]]=vnsoDict.get(row[2],{row[0]:[[row[1],row[3]]]})
        if row[0] not in list(vnsoDict[row[2]].keys()):
            vnsoDict[row[2]][row[0]]=[[row[1],row[3]]]
        else:
            vnsoDict[row[2]][row[0]].append([row[1],row[3]])
            vnsoDict[row[2]][row[0]]=list(set([",".join(item) for item in vnsoDict[row[2]][row[0]]]))
            vnsoDict[row[2]][row[0]]=[item.split(",") for item in vnsoDict[row[2]][row[0]]]
    # print(sorted(list(vnsoDict.keys())))    

    with open("data/topicWordDict.pkl","rb") as topicWordDictFile:
        topicWordDict=pkl.load(topicWordDictFile)
    # print(topicWordDict)
    # print("===============")

    cvnsoDict={}
    for keyItem in cvDict.keys():
        cvnsoDict[keyItem]=cvnsoDict.get(keyItem,{})
        for verbI in range(len(cvDict[keyItem])):
            if cvDict[keyItem][verbI] in vnsoDict.keys():
                ####################
                cvnsoDict[keyItem][cvDict[keyItem][verbI]]=vnsoDict[cvDict[keyItem][verbI]]

    for keyItem in cvnsoDict.keys():
        print("keyItem:",len(list(cvnsoDict[keyItem].keys())))

    nodeList=[]
    edgeList=[]
    nodeRecord={}
    
    nodeRecord["trade war"]=0
    nodeList.append({"name":"trade war",\
            "content":"root",\
            "type":"level0",\
            "ID":0})
    nodeI=1
    for keyItem in cvnsoDict.keys():
        nodeList.append({"name":"cluster-"+str(keyItem),\
                        "content":"cluster",\
                        "type":"level1",\
                        "ID":nodeI})
        ci=nodeI
        nodeRecord[keyItem]=ci

        nodeI+=1
        
        edgeList.append({"source":0,\
                            "target":ci,\
                            "type":"level1",\
                            "marker_type":"topic"})
        with tqdm.tqdm(cvnsoDict[keyItem].keys()) as t:
            for vKeyItem in t:
                if vKeyItem not in nodeRecord.keys():
                    
                    nodeList.append({"name":str(vKeyItem),\
                                    "content":"event",\
                                    "type":"level2",\
                                    "ID":nodeI})
                    vi=nodeI
                    nodeRecord[vKeyItem]=vi

                    nodeI+=1
                else:
                    vi=nodeRecord[vKeyItem]
                edgeList.append({"source":ci,\
                                    "target":vi,\
                                    "type":"level2",\
                                    "marker_type":"event"})
                    
                for newsItem in cvnsoDict[keyItem][vKeyItem].keys():
                    if newsItem not in nodeRecord:
                        cursor.execute("select main_new.title,main_new.time,main_new.article\
                                            from main_new\
                                            where main_new.uid='{}'\
                                            limit 1;".format(newsItem))
                        newsTitle,newsTime,newsArticle=cursor.fetchone()
                        nodeList.append({"name":newsTitle,\
                                        "type":"level3",\
                                        "content":"{"+newsTime+":"+newsTitle+"}"+newsArticle,\
                                        "ID":nodeI})
                        ni=nodeI
                        nodeRecord[newsItem]=ni

                        nodeI+=1
                    else:
                        ni=nodeRecord[newsItem]
                    edgeList.append({"source":vi,\
                                        "target":ni,\
                                        "type":"level3",\
                                        "marker_type":"event",\
                                        "line_text":"behavior"})
                    

                    for eventItem in cvnsoDict[keyItem][vKeyItem][newsItem]:


                        cursor.execute("select sentence_new.sentence_item \
                                        from sentence_new \
                                        where uid='{}' \
                                        and sentence_item like '%{}%' \
                                        and sentence_item like '%{}%' \
                                        limit 1;".format(newsItem,eventItem[0],vKeyItem,eventItem[1]))
                        newsSentence=cursor.fetchone()
                        if newsSentence is None:
                            cursor.execute("select sentence_new.sentence_item \
                                        from sentence_new \
                                        where uid='{}' \
                                        and sentence_item like '%{}%' \
                                        and sentence_item like '%{}%' \
                                        limit 1;".format(newsItem,eventItem[0],eventItem[1]))
                            newsSentence=cursor.fetchone()
                        if newsSentence is None:
                            cursor.execute("select sentence_new.sentence_item \
                                        from sentence_new \
                                        where uid='{}' \
                                        limit 1;".format(newsItem))
                            newsSentence=cursor.fetchone()
                        if newsSentence is None:
                            newsSentence="{"+newsTime+":"+newsTitle+"}"+newsArticle

                        subjectItem=eventItem[0]
                        if  subjectItem not in nodeRecord.keys():
                            nodeList.append({"name":subjectItem,\
                                            "type":"level4",\
                                            "content":newsSentence,\
                                            "ID":nodeI})
                            si=nodeI
                            nodeRecord[subjectItem]=si

                            nodeI+=1
                        else:
                            si=nodeRecord[subjectItem]

                        edgeList.append({"source":ni,\
                                        "target":si,\
                                        "type":"level4",\
                                        "marker_type":"subject",\
                                        "line_text":"subject"})

                        objectItem=eventItem[1]

                        if objectItem not in nodeRecord.keys():
                            nodeList.append({"name":objectItem,\
                                            "content":newsSentence,\
                                            "type":"level5",\
                                            "ID":nodeI})
                            oi=nodeI
                            nodeRecord[objectItem]=oi

                            nodeI+=1
                        else:
                            oi=nodeRecord[objectItem]

                        edgeList.append({"source":si,\
                                        "target":oi,\
                                        "type":"level5",\
                                        "marker_type":"object",\
                                        "line_text":"object"})

        with open(str(keyItem)+"-Node.pkl","wb+") as nodeListFile:
            pkl.dump(nodeList,nodeListFile)
        with open(str(keyItem)+"-Edge.pkl","wb+") as edgeListFile:
            pkl.dump(edgeList,edgeListFile)

    graphPkl={
        "trade war":
        {
            "nodes":nodeList,
            "edges":edgeList
        }
    }

    with open("AD/knowledge_graphs/data/graphPkl.pkl","wb+") as graphPklFile:
        pkl.dump(graphPkl,graphPklFile)