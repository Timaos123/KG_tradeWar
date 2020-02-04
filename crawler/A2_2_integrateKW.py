#coding:utf8

import pandas as pd
import numpy as np
import tqdm
import re

if __name__=="__main__":
    
    originalDf=pd.read_csv("data/originalData.csv",sep="|")
    
    ukwList=originalDf.loc[:,["uid","keywords"]].astype("str").values.tolist()

    newUKWList=[]
    for row in tqdm.tqdm(ukwList):
        if "None" not in row[1] and "[]" not in row[1] and "nan" not in row[0] and "nan" not in row[1]:
            row1=eval(row[1])
            for kwItem in row1:
                newUKWList.append([row[0],kwItem])

    ukwDf=pd.DataFrame(np.array(newUKWList),columns=["uid","keywords"])
    ukwDf.to_csv("data/keyword_table.csv",index=None)
    