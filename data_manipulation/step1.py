__author__ = 'quek'


import requests
import json

base_url = "http://129.94.136.200/"
ensembl_api = "ensembl.json?ids="
upJsonFile = 'sample_data/vaDown.txt'
downJsonFile= 'sample_data/vaUp.txt'






def makeJsonCall(id):
    if isinstance(id, list):
        id = ",".join(id)
    full_url = "%s%s%s" % (base_url, ensembl_api, id)
    print full_url
    response = requests.get(full_url)
    return response.json()

def readAndCall(filename):
    idList = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            fields= line.split('\t')
            idList.append(fields[1])
    return makeJsonCall(idList)


db_list = ['ids', 'GO-BP','GO-MF','GO-CC','Wiki','Disease']



with open('up.json', 'w+') as f:
    upJson = readAndCall(upJsonFile)
    subJson = {k: upJson[k] for k in db_list}
    json.dump(subJson, f, indent=4,  separators=(',',':'))

with open('down.json', 'w+') as f:
    downJson = readAndCall(downJsonFile)
    subJson = {k: downJson[k] for k in db_list}
    json.dump(subJson, f, indent=4,  separators=(',',':'))













