#!/usr/bin/env python
# -*- coding: utf-8

# Dmitry Abramov
# Python v. 2.7.9

from __future__ import print_function
import numpy as np
from preprocessing.tokenize_and_stem import tokenize_and_stem
from Scraper import Scraper, search_articles

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

num_clusters = 7


class kMeansClustering:
    def __init__(self, snippets):
        self.snippets = snippets
        self.clusters = []
    
    def find_clusters(self):  
    
        #define vectorizer parameters
        tfidf_vectorizer = TfidfVectorizer(max_df=0.999, max_features=200000,
                                 min_df=0.001, stop_words='english',
                                 use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,1))
        tfidf_matrix = tfidf_vectorizer.fit_transform(self.snippets) #fit the vectorizer to synopses
        terms = tfidf_vectorizer.get_feature_names()
        matrix = tfidf_matrix.todense()

        km = KMeans(n_clusters=num_clusters)
        km.fit(tfidf_matrix)
        
        self.clusters = km.labels_.tolist()     
        return self.clusters
        
    def print_clusters(self):
        for i in range(num_clusters):
            print("cluster #%i contains documents:" % (i))
            for j, cluster in enumerate(self.clusters):
                if cluster == i:
                    print(j, end=', ')
            print('\n')

def main():
    guardURL = 'http://content.guardianapis.com/search?'
    nytURL = 'http://api.nytimes.com/svc/search/v2/articlesearch.json?'
    key_g = ' ' # insert your guardian api-key
    key_nyt = ' ' # #insert your nyt api-key
    
    urls = [guardURL, nytURL]
    keys = [key_g, key_nyt] 
    query = "obama"
    
    snippets = search_articles(urls, keys, query)
    if len(snippets) == 0:
        return
    km = kMeansClustering(snippets)
    km.find_clusters()
    km.print_clusters()
    
if __name__ == "__main__":
    main()
