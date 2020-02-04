#coding:utf8

import pandas as pd
import numpy as np
import tqdm

if __name__=="__main__":

    originDf=pd.read_csv("data/originalData.csv",sep="|")

    originUidList=originDf["uid"].values.tolist()

    originSenTList=[]
    for uidItem in tqdm.tqdm(originUidList):
        try:
            tmpSenTList=originDf.loc[originDf["uid"]==uidItem,"article"].values.tolist()[0].split(".")
            tmpSenTList=[senT.replace("\n","") for senT in tmpSenTList if len(senT.split(" "))>=5]
            # keep sentences with more than 5 words

            for tmpSenT in tmpSenTList:
                originSenTList.append([uidItem,tmpSenT])
        except Exception as ex:
            print(uidItem,str(ex))
    
    newSentDf=pd.DataFrame(np.array(originSenTList),columns=["uid","sentence item"])

    newSentDf.to_csv("data/sentence_table.csv",index=None)