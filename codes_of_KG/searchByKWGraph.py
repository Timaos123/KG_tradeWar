#coding:utf8
'''
Created on 2018年7月10日

@author: Administrator
'''
import pickle as pkl
import json
import tqdm
import numpy as np
# import enchant

from nltk import SnowballStemmer
from nltk import WordNetLemmatizer
from nltk.corpus import wordnet

def stem(sentence):
  """
  input: raw sentence 
  process:Stemming
  output: new sentence
  """
  myStemmer = SnowballStemmer("english")
  sentence=sentence.lower()
  lemmatizer = WordNetLemmatizer()
  
  sentence=" ".join([lemmatizer.lemmatize(word)\
                      if len(wordnet.synsets(lemmatizer.lemmatize(word)))>0 and wordnet.synsets(lemmatizer.lemmatize(word))[0].name().startswith(lemmatizer.lemmatize(word))==True\
                          else word \
                      for word in sentence.split(" ")])
  sentence=" ".join([myStemmer.stem(word)\
                      if len(wordnet.synsets(myStemmer.stem(word)))>0 and wordnet.synsets(myStemmer.stem(word))[0].name().startswith(myStemmer.stem(word))==True\
                          else word \
                      for word in sentence.split(" ")])
  
  return sentence

# def correctWord(word):
#     spell_dict = enchant.Dict("en_US")
#     max_dist = 2
#     if spell_dict.check(word) == False:
#         suggestions = spell_dict.suggest(word)
#     if suggestions and edit_distance(word, suggestions[0])<=max_dist:
#         nword=suggestions[0]
#     else:
#         nword=word
#     return nword

def match(word,checkList):
    maxLenArr=np.array([max([len(word),len(checkItem)]) for checkItem in checkList])
    maxMatchLenArr=np.array([min(len(word),len(checkItem))\
                                if word in checkItem or\
                                    checkItem in word 
                                else\
                                    len([i\
                                    for i in range(min(len(word),len(checkItem)))\
                                    if word[i]==checkItem[i]
                                ])for checkItem in checkList])
    maxMatchLenArr=maxMatchLenArr/(maxLenArr+0.01)
    return maxMatchLenArr

def main(searchWord):
    searchWord=stem(searchWord)
    searchWordList=searchWord.split()
    # searchWordList=[correctWord(wordItem) for wordItem in searchWord.split()]
    newDict={"search":{"edges":[],"nodes":[]}}
    sourcePkl="AD/knowledge_graphs/data/graphPkl.pkl"
    targetPkl="AD/knowledge_graphs/data/searchGraphPkl.pkl"
    nodeList=[]

    print("integrate the searched words ...")
    with open(sourcePkl,"rb") as sourcePklFile:
        originDict=pkl.load(sourcePklFile)
    
    nodeList=originDict[list(originDict.keys())[0]]["nodes"]
    edgeList=originDict[list(originDict.keys())[0]]["edges"]

    print("integrate the new graph ...")
    matchDegreeList=[match(wordItem,[nodeItem["name"] for nodeItem in nodeList])
                        for wordItem in searchWordList]
    searchWordIndexList=[np.argmax(dList) for dList in matchDegreeList]

    sourceWordIndexList=[edgeItem["source"]\
                        for edgeItem in originDict[list(originDict.keys())[0]]["edges"]\
                        if edgeItem["target"] in searchWordIndexList]
    
    targetWordIndexList=[edgeItem["target"]\
                        for edgeItem in originDict[list(originDict.keys())[0]]["edges"]\
                        if edgeItem["source"] in searchWordIndexList]

    sourceNode=[edgeItem["target"] for edgeItem in originDict[list(originDict.keys())[0]]["edges"]]

    newNodeIndexList=list(set(sourceWordIndexList+searchWordIndexList+targetWordIndexList))

    print("saving data ...")
    edgeList=[{
                    "source":newNodeIndexList.index(edgeItem["source"]),\
                    "target":newNodeIndexList.index(edgeItem["target"]),\
                    "type":"level1",\
                    "marker_type":"search"         
                }
                for edgeItem in edgeList\
                if edgeItem["source"] in newNodeIndexList and\
                    edgeItem["target"] in newNodeIndexList]
    nodeList=[nodeList[nodeI]
                for nodeI in newNodeIndexList
            ]

    newDict={
        "search":
        {
            "nodes":nodeList,
            "edges":edgeList
        }
    }

    with open(targetPkl,"wb") as newDictFile:
        pkl.dump(newDict,newDictFile)

if __name__=="__main__":

    searchWord="fung growth"

    main(searchWord)