__author__ = 'chunxiao'

import json
import requests

base_url = "http://129.94.136.200/"
pubmed_api = "pubmed.json?ids="
step1_result_file = "sample_data/up.json"

db_list = ['GO-BP','GO-MF','GO-CC','Wiki','Disease']

from pprint import pprint

terms = []
with open('sample_data/up.json', 'r') as f:
    data = json.load(f)
    for db in db_list:
        for term in data[db]:
            terms.append(term)
# pprint(terms)

articles = []
with open(step1_result_file, 'r') as f:
    data = json.load(f)
    articles = data['ids']
# pprint(articles)

def makeJsonCall(id):
    if isinstance(id, list):
        id = ",".join(id)
    full_url = "%s%s%s" % (base_url, pubmed_api, id)
    print full_url
    response = requests.get(full_url)
    return response.json()

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
pprint(terms2articles)
