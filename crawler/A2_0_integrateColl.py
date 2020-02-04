#coding:utf8

import pandas as pd

if __name__=="__main__":
    firstPartDf=pd.read_csv("data/collectiveresults1.csv",sep="|").rename({"artcle":"article"},axis="columns",errors="raise")
    secondPartDf=pd.read_csv("data/collectiveresults2.csv",sep="|").rename({"artcle":"article"},axis="columns")
    thirdPartDf=pd.read_csv("data/originalData1.csv",sep="|").rename({"artcle":"article"},axis="columns")

    newDf=pd.concat([firstPartDf,secondPartDf,thirdPartDf],axis=0)

    #basic preprocessing
    newDf.drop_duplicates(inplace=True)
    newDf=newDf.apply(lambda x:x.astype("str").apply(lambda xi:xi.replace(",,","".replace("  ","").replace("\n",""))))
    print(newDf.shape)
    newDf.to_csv("data/originalData.csv",sep="|",index=None)