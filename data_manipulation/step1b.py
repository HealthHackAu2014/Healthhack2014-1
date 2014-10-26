__author__ = 'quek'
from step1 import makeJsonCall
import json
from step2 import collatesDataJson
from pprint import pprint




idList = ['ENSP00000362705','ENSP00000256413','ENSP00000371690','ENSP00000458989','ENSP00000308318']





db_list = ['ids', 'GO-BP','GO-MF','GO-CC','Wiki','Disease']
base_url = "http://129.94.136.200/"
ensembl_api = "ensembl.json?ids="

finalout = {}


for x in idList:
    results = makeJsonCall(x, base_url, ensembl_api )
    subJson = {k: results[k] for k in db_list}
    finalout[x] = subJson

pprint(finalout)


"""
with open('sample_data/five_genes.json', 'w+') as f:
    json.dump(finalout, f, indent=4, separators=(',',':')  )
"""



step2_out = {}

for keys, value in finalout.iteritems():
    step2_out[keys] = collatesDataJson(value)


with open('sample_data/five_description.json', 'w+') as f:
    json.dump(step2_out, f, indent=4,  separators=(',',':'))






