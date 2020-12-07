import requests, json, os
from elasticsearch import Elasticsearch, helpers, client
res = requests.get('http://192.168.43.75:9200')
print (res.content)
es = Elasticsearch([{'host': '192.168.43.75', 'port': '9200'}])
with open('ethereum_1_2gb.json', 'r') as file:  # Use file to refer to the file object

    docket_content = file.read()
    body=json.loads(docket_content)
    with open("app.json", 'w') as f:
        # for i in range(len(body)):
        #     a = {"index": {"_index": "myapp", "_type": "_doc", "_id": i}}
        #     json.dump(a,f)
        #     json.dump(body[i],f)
        resp = helpers.bulk(
                es,
                body,
                index = "ethereum",
                doc_type = "_doc"
                )
        # print ("helpers.bulk() RESPONSE:", resp)
        # print ("helpers.bulk() RESPONSE:", json.dumps(resp, f, indent=4))
    #print(type(body[0]))
    # for i in range(len(body)):
    #     es.index(index='ethereum', ignore=400, doc_type='_doc', 
    #     id=i, body=body[i])

