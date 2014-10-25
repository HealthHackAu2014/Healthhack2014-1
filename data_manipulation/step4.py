__author__ = 'chunxiao'

import json
import requests

base_url = "http://129.94.136.200/"
pubmed_api = "pubmed.json?ids="
step1_results = ["sample_data/up.json", "sample_data/down.json"]

db_list = ['GO-BP','GO-MF','GO-CC','Wiki','Disease']

# from pprint import pprint

def makeJsonCall(id):
    if isinstance(id, list):
        id = ",".join(id)
    full_url = "%s%s%s" % (base_url, pubmed_api, id)
    print full_url
    response = requests.get(full_url)
    return response.json()

def makeTerms2Articles(file):
    terms = []
    with open(file, 'r') as f:
        data = json.load(f)
        for db in db_list:
            for term in data[db]:
                terms.append(term)
    
    articles = []
    
    with open(file, 'r') as f:
        data = json.load(f)
        articles = data['ids']
    
    terms2articles = {}

    for article in articles:
        data = makeJsonCall(article)
        for db in db_list:
            if(db in data):
                for term in data[db]:
                    if(term in terms):
                        if(term in terms2articles):
                            terms2articles[term].append(article)
                        else:
                            terms2articles[term] = [article]

    with open(file+".terms2articles.json", 'w+') as f:
        json.dump(terms2articles, f, indent=4,  separators=(',',':'))

for file in step1_results:
    makeTerms2Articles(file)
