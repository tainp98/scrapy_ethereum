import requests, json, os
from elasticsearch import Elasticsearch
res = requests.get('http://192.168.43.75:9200')
print (res.content)
es = Elasticsearch([{'host': '192.168.43.75', 'port': '9200'}])
i = 1
with open('ethereum.json', 'r') as file:  # Use file to refer to the file object

    docket_content = file.read()
    body=json.loads(docket_content)
    print(type(body[0]))
    for i in range(len(body)):
        es.index(index='ethereum', ignore=400, doc_type='_doc', 
        id=i, body=body[i])