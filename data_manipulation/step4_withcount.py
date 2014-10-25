__author__ = 'chunxiao'

import json
import requests
import os

base_url = "http://129.94.136.200/"
pubmed_api = "pubmed.json?ids="

local_article_cache = "sample_data/local_articles.json"

step1_results = ["sample_data/up.json", "sample_data/down.json"]

db_list = ['GO-BP','GO-MF','GO-CC','Wiki','Disease']

from pprint import pprint

def makeJsonCall(id):
    if isinstance(id, list):
        id = ",".join(id)
    full_url = "%s%s%s" % (base_url, pubmed_api, id)
    print full_url
    response = requests.get(full_url)
    return response.json()

# for all terms in an article, accumulate all counts of these terms from the 
# ensembl.json result, and use this sum to rank articles 

def makeTerms2Articles(file):
    if(os.path.exists(local_article_cache)):
        with open(local_article_cache, 'r') as f:
            local_articles = json.load(f)
    else:
        local_articles = {}
    #pprint(local_articles)
    terms = {}
    with open(file, 'r') as f:
        data = json.load(f)
        for db in db_list:
            if(db in data):
                for term in data[db]:
                    terms[term] = data[db][term]
    
    articles = {}
    
    with open(file, 'r') as f:
        data = json.load(f)
        for article in data['ids']:
            articles[article] = 0
    
    terms2articles = {}

    for article in articles:
        if(str(article) in local_articles):
            data = local_articles[str(article)]
        else: 
            data = makeJsonCall(article)
            local_articles[article] = data

        count = 0;
        for db in db_list:
            if(db in data):
                for term in data[db]:
                    if(term in terms):
                        count += terms[term]
        articles[article] = count

        for db in db_list:
            if(db in data):
                for term in data[db]:
                    if(term in terms):
                        if(term in terms2articles):
                            terms2articles[term].append((article, articles[article]))
                        else:
                            terms2articles[term] = [(article, articles[article])]
    for term in terms2articles:
        terms2articles[term] = sorted(terms2articles[term], key=(lambda article: article[1]), reverse=True)
 
    with open(file+".terms2articles_count.json", 'w+') as f:
        json.dump(terms2articles, f, indent=4,  separators=(',',':'))
    with open(local_article_cache, 'w') as f:
        json.dump(local_articles, f, indent=4,  separators=(',',':'))

for file in step1_results:
    makeTerms2Articles(file)
