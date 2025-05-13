import boto3
import base64
import json

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    for record in event['Records']:
        payload = base64.b64decode(record["kinesis"]["data"])
        # Process the payload and save to S3
        s3_client.put_object(
            Bucket='my-unique-bucket-name-xyz',
            Key='video-frame.jpg',
            Body=payload
        )
    return {
        'statusCode': 200,
        'body': json.dumps('Video processed successfully')
    }
