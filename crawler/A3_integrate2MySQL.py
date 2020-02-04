#coding:utf8

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

def rmSpecialMark(sentence):
    if "\ufeff" in sentence:
        sentence=sentence.replace("\ufeff","")
    return " ".join(sentence.split(" ")[:5000])

if __name__=="__main__":

    engine_loacl = create_engine('mysql+pymysql://my7012:my7012@39.107.92.174/my7012', echo=True)

    originDf=pd.read_csv("data/originalData.csv",sep="|")
    keywordDf=pd.read_csv("data/keyword_table.csv")
    sentenceDf=pd.read_csv("data/sentence_table.csv")

    originDf=originDf.apply(lambda x:x.astype("str").apply(lambda xi:rmSpecialMark(xi)))
    keywordDf=keywordDf.apply(lambda x:x.astype("str").apply(lambda xi:rmSpecialMark(xi)))
    sentenceDf=sentenceDf.apply(lambda x:x.astype("str").apply(lambda xi:rmSpecialMark(xi)))


    originDf.to_sql("main_table",engine_loacl,"my7012",if_exists="replace",index_label="uid",index=False)
    keywordDf.to_sql("keyword_table",engine_loacl,"my7012",if_exists="replace",index=True)
    sentenceDf.to_sql("sentence_table",engine_loacl,"my7012",if_exists="replace",index=True)

    # tmpDf=pd.read_sql().loc[:5,:]
    # print(tmpDf)