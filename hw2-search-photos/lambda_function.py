import json
import boto3
import requests


host = "https://search-hw2-photos-nja2frnmhqhc4wziglhbha4e6u.us-east-1.es.amazonaws.com"
index = "photos"
service = 'es'
url = host + "/" + index + "/_search"
headers = { "Content-Type": "application/json" }


def lambda_handler(event, context):
    print(event)
    q = event['q']
    client = boto3.client("lex-runtime")
    res = client.post_text(
        botName = 'searchPhotoBot',
        botAlias = 'search',
        userId = '22',
        inputText = q
    )
    if not 'slots' in res:
        return {
            'statusCode': 404,
            'body': []
        }
    keys = []
    for key, val in res['slots'].items():
        if val:
            keys.append(val)
    print(keys)

    es_query = []
    photos = set()
    for k in keys:
        es_query.append(k)
        query = {
            "size": 2000,
            "query": {
                "multi_match": {
                    "query": k,
                    "fields" : ['labels']
                }
            }
        }
        rep = requests.get(url, auth=("admin", "Luyuan1998213."), headers=headers, data=json.dumps(query))
        rep_json = rep.json()
        print(rep_json)

        for each in rep_json['hits']['hits']:
            objectKey = each['_source']['objectKey']
            bucket = each['_source']['bucket']
            image_url = "https://" + bucket + ".s3.amazonaws.com/" + objectKey
            photos.add(image_url)

    return {
        'statusCode': 200,
        'headers':{
            'Access-Control-Allow-Origin':'*',
            'Access-Control-Allow-Credentials':True
        },
        'body': {"results":list(photos)}
    }



    # ---------------- query in the open search ------------------
    # query = {
    #     "size": 2000,
    #     "query": {
    #         "multi_match": {
    #             "query": "dog OR person",
    #             "fields" : ["labels"]
    #         }
    #     }
    # }

    # return{
    #     'statusCode': 200,
    #     'body': json.dumps('Hello from Lambda')
    # }
