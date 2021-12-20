from __future__ import unicode_literals
from hazm import *
import pandas as pd
import math
import heapq
import numpy as np


class UniversalSet(set):
    def __and__(self, other):
        return other

    def __rand__(self, other):
        return other


class DocTerm:

 def __init__(self,docId):
  self.docId = docId
  self.positions = []
  self.freq=0
  self.weight=0

 def insert(self, position):
  self.positions.append(position)
  self.positions = sorted(self.positions)
  self.freq+=1

 def __eq__(self, other):
     return self.weight==other.weight

 def __lt__(self, other):
     if self.weight<other.weight:return True
     else:return False

 def __gt__(self, other):
     if self.weight > other.weight:
         return True
     else:
         return False


class Term:

 def __init__(self, id):

  self.id = id
  self.docIds=[]
  self.docTerms = dict()
  self.championsList=[]

 def insert(self, docId, position):
  if docId not in self.docTerms.keys():
   self.docTerms[docId] = DocTerm(docId)
  self.docTerms[docId].insert(position=position)

 def updateLists(self):
     self.championsList=sorted(self.docTerms.values(),reverse=True)
     self.docIds=sorted(self.docTerms.keys())

 def updateWeights(self,N):
     print()
     for docIds in self.docTerms.keys():
         doc = self.docTerms[docIds]
         print()
         doc.weight = calculateTfIdf(doc.freq, N, len(self.docTerms))
         print()


class Index:

 def __init__(self):
  self.index = dict()
  self.termAxis=[]
  self.tokenCount=0
  self.termCount=0
  self.docs=dict()

 def indexInsert(self,term,docId,position):
     self.tokenCount += 1
     if not docId in self.docs.keys():
         self.docs[docId]=set()
     if term not in self.index.keys():
         self.index[term] = Term(id=term)
         self.termCount += 1
     self.docs[docId].add(term)
     self.index[term].insert(docId=docId, position=position)
     self.termAxis.append(self.termCount)
     #print()

 def updateListsAndDocVectors(self):

     for termId in self.index.keys():
         self.index[termId].updateWeights(len(self.docs))

     for termId in self.index.keys():
         self.index[termId].updateLists()



def calculateTfIdf(termFreq,indexSize,docFreq):
    tf=(1+math.log10(termFreq))
    idf=math.log10(indexSize/docFreq)
    print()
    return tf*idf

def rankedQueryResults(index,query,k,r):

    queryTerms = preProcessor(query)
    queryWeights=dict()
    docs=set()
    score = dict()
    length = dict()
    print()

    for term in queryTerms:
        freq=queryTerms.count(term)
        queryWeights[term]=calculateTfIdf(freq,len(index.docs),len(index.index[term].docTerms))
        #queryWeights[term] = calculateTfIdf(freq, 10, 1)
        if term in index.index.keys():
         champions=index.index[term].championsList
         if r<len(champions):champions=champions[0:r]
         docs=docs | set([champion.docId for champion in champions])

    #queryLength=np.sqrt(np.sum(np.power(list(queryWeights.values()),2)))
    queryLength=np.linalg.norm(list(queryWeights.values()))
    #queryLength=1

    if len(docs)<k:
        neededDocs=k-len(docs)
        for i in range(0,neededDocs):
         for term in queryTerms:
             if len(docs)>=k:break
             if term in index.index.keys():
                 champions = index.index[term].championsList
                 if r+i<len(champions):
                  champion = champions[r+i]
                  docs.add(champion.docId)

    docs=heapq.nlargest(k,docs)
    print()
    for doc in docs:
        docTermSet= index.docs[doc]
        print()
        for term in docTermSet:
         if term in queryTerms:
              if not doc in score:
                  score[doc]=0
                  length[doc]=0
              weight=index.index[term].docTerms[doc].weight
              score[doc]+=weight*queryWeights[term]
              print()
              length[doc]+=math.pow(weight,2)

    print()
    for docId in score.keys():
        score[docId]=score[docId]/(math.sqrt(length[docId])*queryLength)

    score=[(key,score[key]) for key in score.keys()]
    score=sorted(score,key=lambda x:x[1],reverse=True)
    score=[temp[0] for temp in score]
    print()
    return score



def preProcessor(text,haveStopWords=False,haveStemming=True):
 stemmer = Stemmer()
 normalizer = Normalizer()
 tokens = word_tokenize(text)
 stopWords=stopwords_list()
 finalTokens=[]

 for i in range(len(tokens)):
     if (tokens[i] not in stopWords) or haveStopWords:
      normalTemp = normalizer.normalize(tokens[i])
      if haveStemming:stemTemp=stemmer.stem(normalTemp)
      else:stemTemp=normalTemp
      finalTokens.append(stemTemp)

 return finalTokens


def tokenMerger(tokens):
    mergedToken=''

    for i in range(len(tokens)):
        mergedToken+=" "+tokens[i]

    return mergedToken

def indexer(index,docs,ids,haveStopWords=False,haveStemming=True):

    for i in range(len(docs)):
        doc = preProcessor(docs[i],haveStopWords=haveStopWords,haveStemming=haveStemming)
        #print()
        for j in range(len(doc)):
            term = doc[j]
            index.indexInsert(term,ids[i],j)

    print("done")

def getOrderedFreqsOfTerms(Index):
    freqs=[]
    rankedTerms = sorted(Index.index.values())
    print()
    for i in range(len(rankedTerms)):
        freqs.append(rankedTerms[i].freq)
    return freqs

def idMaker(urls):
    ids=[]
    for i in range(len(urls)):
        ids.append(int(urls[i].split("/")[4]))
    return list(ids)

def idTransDictMaker(ids):
    idTransDict=dict()
    for i in range(len(ids)):
        idTransDict[ids[i]]=i
    return idTransDict



docsDatabaseFileName="IR1_7k_news100.xlsx"
maxSize=8000
#query="دانشگاه صنعتی امیرکبیر"
query=input("پرسمان را وارد کنید")
dataSize=maxSize
haveStopWords=False
haveStemming=True

table = pd.read_excel(docsDatabaseFileName,)
docs=list(table['content'][0:dataSize])
titles=list(table['title'][0:dataSize])
urls=list(table['url'][0:dataSize])
ids=idMaker(urls)
print()
idTransDict=idTransDictMaker(ids)
print()
fileIndex = Index()

indexer(fileIndex,docs,ids,haveStopWords=haveStopWords,haveStemming=haveStemming)
fileIndex.updateListsAndDocVectors()

#results = queryResults(fileIndex.index, query)

results = rankedQueryResults(fileIndex,query,10,1)

print("تعداد اسناد بازیابی شده برابر است با:")
print(len(results))

for i in range(len(results)):
         print("شناسه سند:")
         print(results[i])
         print("تیتر:")
         print(titles[idTransDict[results[i]]])
         print("---------------------------------------------------------------------------------")








