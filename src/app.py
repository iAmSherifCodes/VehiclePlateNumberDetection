import json
import boto3
import os

def detect_text(photo, bucket):
    session = boto3.Session(os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'], os.environ['AWS_SESSION_TOKEN'])
    client = session.client('rekognition')

    response = client.detect_text(Image={'S3Object': {'Bucket': bucket, 'Name': photo}})
    best_text = ""

    textDetections = response['TextDetections']
    print('Detected text\n----------')
    for text in textDetections:
        detected_text = text['DetectedText']
        print('Detected text:' + detected_text)
        print('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")
        print('Id: {}'.format(text['Id']))
        if 'ParentId' in text:
            print('Parent Id: {}'.format(text['ParentId']))
        print('Type:' + text['Type'])
        print()
        if len(detected_text) >= 7:
            best_text = detected_text

    return str(best_text)

def handler(event, context):
    photo = event['photo']
    bucket = event['bucket']
    text = detect_text(photo=photo, bucket=bucket)
    return {
        "body": json.dumps({
            "result": text,
        }),
    }
