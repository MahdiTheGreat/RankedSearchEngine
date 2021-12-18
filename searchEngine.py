from __future__ import unicode_literals
from hazm import *
import pandas as pd
import math
import bisect


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
  self.docTerms = dict()
  self.championsList=[]

 def insert(self, docId, position):
  if docId not in self.docTerms.keys():
   self.docTerms[docId] = DocTerm(docId)
   bisect.insort(self.championsList, docId)
  self.docTerms[docId].insert(position=position)


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

 def calculateTfIdf(self):
     termIds=self.index.keys()
     for termId in termIds:
         term=self.index[termId]
         docTerms=term.docTerms
         print()
         for docIds in docTerms.keys():
             doc=docTerms[docIds]
             print()
             doc.weight=calculateTfIdf(doc.freq,len(self.docs.keys()),len(term.docTerms))
             print()

def calculateTfIdf(termFreq,indexSize,docFreq):
    tf=(1+math.log10(termFreq))
    idf=math.log10(indexSize/docFreq)
    print()
    return tf*idf

#def rankedQueryResults(index,query,k,r):
#    score=dict()
#    length=dict()
#    terms = preProcessor(query)
#    queryWeights=dict()
#
#    for term in terms:
#        freq=terms.count(term)
#        queryWeights[term]=calculateTfIdf(freq,10,1)
#
#    for term in terms:
#        term=index.index[term]
#        if r<len(term.champions):
#         docTerms=term.champions[0:r]
#        else:
#            docTerms = term.champions
#        print()
#        for docTerm in docTerms:
#            docId=docTerm.id
#            if docId not in score.keys():
#                score[docId]=0
#                length[docId]=0
#            score[docId]+=docTerm.weight*queryWeights[term]
#            length[docId]+=math.pow(docTerm.weight,2)
#
#    for docId in score.keys():
#        score[docId]=score[docId]/np.sqrt(length[docId])
#
#    score=[(key,score[key]) for key in score.keys()]
#    score=sorted(score,key=lambda x:x[1])
#    score=[temp[0] for temp in score]
#
#    return score

def rankedQueryResults(index,query,k,r):
    score=dict()
    length=dict()
    queryTerms = preProcessor(query)
    queryWeights=dict()
    docs=set()
    print()

    for term in queryTerms:
        freq=queryTerms.count(term)
        queryWeights[term]=calculateTfIdf(freq,10,1)
        if term in index.index.keys():
         champions=index.index[term].championsList
         if r<len(champions):champions=champions[0:r]
         docs=docs | set(champions)

    docs=list(docs)
    score=dict()
    length=dict()
    for doc in docs:
        for term in queryTerms:
            if not doc in score:
                score[doc]=0
                length[doc]=0
            weight=index.index[term].docTerms[doc].weight
            score[doc]+=weight*queryWeights[term]
            print()
            length[doc]+=math.pow(weight,2)

    for docId in score.keys():
        score[docId]=score[docId]/math.sqrt(length[docId])

    score=[(key,score[key]) for key in score.keys()]
    score=sorted(score,key=lambda x:x[1])
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
    ids=set()
    for i in range(len(urls)):
        ids.add(int(urls[i].split("/")[4]))
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
fileIndex.calculateTfIdf()

#results = queryResults(fileIndex.index, query)

results = rankedQueryResults(fileIndex,query,5,4)

print("تعداد اسناد بازیابی شده برابر است با:")
print(len(results))

for i in range(len(results)):
         print("شناسه سند:")
         print(results[i])
         print("تیتر:")
         print(titles[idTransDict[results[i]]])
         print("---------------------------------------------------------------------------------")








