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
# ensembl.json result, and use this sum for article weights
def getArticleWeight(query_terms, article_json):
    count = 0;
    for db in db_list:
        if(db in article_json):
            for term in article_json[db]:
                if(term in query_terms):
                    count += query_terms[term]
    return count

# multiply article weight with the appreance count of the term in the article 
def getArticleWeightPerTerm(article, term, article_weights, query_terms):
    return article_weights[article] * query_terms[term]

def makeTerms2Articles(file):
    if(os.path.exists(local_article_cache)):
        with open(local_article_cache, 'r') as f:
            local_articles = json.load(f)
    else:
        local_articles = {}

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
            articles[article] = getArticleWeight(terms, data)

    terms2articles = {}
    for article in articles:
        if(str(article) in local_articles):
            data = local_articles[str(article)]
        else: 
            data = makeJsonCall(article)
            local_articles[article] = data

        for db in db_list:
            if(db in data):
                for term in data[db]:
                    if(term in terms):
                        if(term in terms2articles):
                            terms2articles[term].append((article, 
                                                         getArticleWeightPerTerm(article, term, articles, terms)))
                        else:
                            terms2articles[term] = [(article, 
                                                     getArticleWeightPerTerm(article, term, articles, terms))]
    for term in terms2articles:
        terms2articles[term] = sorted(terms2articles[term], key=(lambda article: article[1]), reverse=True)
 
    with open(file+".terms2articles_count.json", 'w+') as f:
        json.dump(terms2articles, f, indent=4,  separators=(',',':'))
    with open(local_article_cache, 'w') as f:
        json.dump(local_articles, f, indent=4,  separators=(',',':'))

for file in step1_results:
    makeTerms2Articles(file)
