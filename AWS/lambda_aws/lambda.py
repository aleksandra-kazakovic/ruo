import json
import boto3
import requests

hostname = "http://ec2-3-74-43-66.eu-central-1.compute.amazonaws.com:5000"
PREDICT_PATH = "/predict"

def lambda_handler(event, context):
    print(event)
  
    if event.get("path"):
        if (event['path'] == PREDICT_PATH):
            try:
                model_name = event['queryStringParameters']['model_name']
                dataset_name = event['queryStringParameters']['dataset_name']
                endpoint = hostname +"/predict?model_name=" +model_name+"&dataset_name="+dataset_name
                response = requests.post(endpoint)
                print(response)
                return {
                    'statusCode': 200,
                    'body': json.dumps(json.loads(response.text))
                }
            except Exception as e:
                print(e)
                
    else:        
        event_type = event['Records'][0]['eventName']
        file_path = event['Records'][0]['s3']['object']['key']
        file_name = file_path.split(".")[0]
                
        if "ObjectCreated" in event_type:
            try:
                endpoint = hostname+"/trainMlModel?file_name=" + file_name
                response = requests.post(endpoint)
                return {
                        'statusCode': 200,
                        'body': json.dumps(response.text)
                    }
            except Exception as e:
                print(e)
    
        elif "ObjectRemoved" in event_type:
            try:
                endpoint = hostname + "/delete?model_name=" + file_name
                response = requests.post(endpoint)
                return {
                    'statusCode': 200,
                    'body': json.dumps(response.text)
                }
                
            except Exception as e:
                print(e)

            