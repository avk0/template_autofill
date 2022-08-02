import base64
import boto3
import json


def lambda_handler(event, context):
    print('Event keys: ' + '; '.join(list(event.keys())))

    if 1:
        try:
            print('File1 name: ', event['fname1'])
            print('File2 name: ', event['fname2'])
            
            file1_base64 = event['file1']
            file1_base64 = file1_base64[file1_base64.find(",")+1:]
            file1 = base64.b64decode(file1_base64)
            print('file1 OK')
            
            file2_base64 = event['file2']
            file2_base64 = file2_base64[file2_base64.find(",")+1:]
            file2 = base64.b64decode(file2_base64)
            print('file2 OK')
            
            s3 = boto3.client('s3')
            s3.put_object(Bucket="autofill-template-s3b", 
                          Key=event['fname1'], 
                          Body=file1)
            s3.put_object(Bucket="autofill-template-s3b", 
                          Key=event['fname2'], 
                          Body=file2)
            
            res = {
                'headers': { "Content-Type": "text/html" },
                'statusCode': 200,
                'body': 'success'
            }
        except Exception as e:
            print(e)
            res = {
                'headers': { "Content-Type": "text/html" },
                'statusCode': 200,
                'body': 'FAILED'
            }

    if 0:
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket="autofill-template-s3b", Key='index.html')
        content = response['Body']
        byte_content = content.read()
        
        res = {
            'headers': { "Content-Type": "text/html" },
            'statusCode': 200,
            'body': base64.b64encode(byte_content).decode('utf-8'),
            'isBase64Encoded': True
        }

    if 0:
        res = {'statusCode': 301,
               'headers': {
                  'Location': 'https://autofill-template-s3b.s3.eu-central-1.amazonaws.com/index.html',
                }
               }

    return res
