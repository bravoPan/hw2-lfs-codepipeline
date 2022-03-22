import json
import boto3
import requests
import urllib.parse
import datetime
from requests_aws4auth import AWS4Auth

# Connect to S3 bucket
s3 = boto3.client('s3')
region = "us-east-1"

# Connect to opensearch for POST
host = "https://search-hw2-photos-nja2frnmhqhc4wziglhbha4e6u.us-east-1.es.amazonaws.com"
index = "photos"
service = 'es'
url = host + "/" + index + "/_doc"
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
headers = { "Content-Type": "application/json" }

def lambda_handler(event, context):
    # rep = requests.get(host)
    # print(rep)

    # # TODO implement
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        res = s3.head_object(Bucket=bucket, Key=key)
        last_modified = response["LastModified"].strftime("%m/%d/%Y, %H:%M:%S")
        rek_client = boto3.client("rekognition")
        rek_resp = rek_client.detect_labels(Image={"Bytes": response["Body"].read()}, MaxLabels=5, MinConfidence=70)
        labels = res["Metadata"]["customlabels"].replace(" ", "").split(",")
        # labels_li = i["Name"].lower() for i in rek_resp["Labels"]
        for i in rek_resp["Labels"]:
            labels.append(i['Name'].lower())
        labels_li = set(labels)
        # def myconverter(o):
        #     if isinstance(o, datetime.datetime):
        #         return o.__str__()
        # jsonfied_date = json.dumps(last_modified, default=myconverter)
        data = {"objectKey": key, "bucket": bucket, "createdTimestamp": last_modified, "labels": list(labels_li)}
        print(data)
        r = requests.post(url, auth=("admin", "Luyuan1998213."), json=data, headers=headers)
        print(r.text)
        # print(jsonfied_date)
        # print(last_modified)
        # print(labels_li)
        # return response['ContentType']
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e


    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
