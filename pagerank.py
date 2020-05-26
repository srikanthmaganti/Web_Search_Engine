# -*- coding: utf-8 -*-
"""
Created on Sun May  5 15:59:17 2019

@author: santh
"""

#name:Santhosh mani
#uin:662957954

import pickle
import os
import json


def QuerydependentPR(tfidf, crawled_pages, inlink, beta=0.85):
    querydependentrank = {}
    for doc in tfidf:
        querydependentrank[doc] = {}
        for term in tfidf[doc]:
            querydependentrank[doc][term] = 1/len(tfidf[doc])
    for iters in range(10):
        co = 0
        for doc in tfidf:
            co += 1
            print(iters,co,doc)
            if iters==10:
                break
            for term in tfidf[doc]:
                s = 0
				#print(term)
                for i in inlink[doc]:
					# if doc in crawled_pages[i][2]:
                    s += (querydependentrank[i][term] if term in querydependentrank[i] else 0) * pqi2j(term, i, doc, tfidf)
                pdash_query = tfidf[doc][term]/sum(tfidf[i][term] if term in tfidf[i] else 0 for i in tfidf)
                querydependentrank[doc][term] = (1 - beta) * pdash_query + (beta * s)
    save_json(querydependentrank, "querydependentrank")
		



def pqi2j(term, i, j, tfidf):#Pq(i→j)  and Pq’(j)  are  arbitrary  distributions,  we  will  focus  on  the  case  where  both probability  distributions  are  derived from query term
	s = 0
	for doc in crawled_pages[i][2]:
		if doc in tfidf and term in tfidf[doc]:
			s += tfidf[doc][term]

	return (tfidf[j][term] if term in tfidf[j] else 0)/s
	

def save_pickle(obj, name):
	with open(name + '.pkl', 'wb') as f:
		pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_pickle(name):
	with open(name + '.pkl', 'rb') as f:
		return pickle.load(f)

def save_json(obj, name):
	j = json.dumps(obj)
	f = open(name+".json", "w")
	f.write(j)
	f.close()

def load(name):
	if os.path.getsize("inlink.pkl") > 0:      
	    with open("inlink.pkl", "rb") as f:
	        unpickler = pickle.Unpickler(f)
	        
	        return unpickler.load()

if __name__ == "__main__":
    
    crawled_pages = load_pickle("crawled_pages")
    tfidf = load_pickle("tfidf")
    if os.path.isfile('inlink.pkl'):
        inlink = load("inlink")
        
    else:
    	inlink = {}
    	c = 0
    	for doc in tfidf:
            c+=1
    	              
            inlink[doc] = []
            for i in crawled_pages:
                if doc in crawled_pages[i][2]:
                    inlink[doc].append(crawled_pages[i][0])
 
    	save_pickle(inlink, "inlink.pkl")
    QuerydependentPR(tfidf, crawled_pages, inlink, 0.85)
