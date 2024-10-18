import json
import boto3
import re
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def detect_text(photo, bucket):
    session = boto3.Session(
        os.environ['AWS_ACCESS_KEY_ID'],
        os.environ['AWS_SECRET_ACCESS_KEY'],
        os.environ['AWS_SESSION_TOKEN'])
    client = session.client('rekognition')

    response = client.detect_text(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': photo}
        }
    )
    plate_number_pattern = re.compile(r"^[A-Z]{2,3}[-\s]?\d{3}[-\s]?[A-Z]{2,3}$")

    textDetections = response['TextDetections']
    for text in textDetections:
        if plate_number_pattern.match(text['DetectedText']):
            return text['DetectedText']

    return "Plate Number Not Found"


def handler(event, context):
    try:
        logger.info(f"Received event: {type(event)}")
        logger.info(f"Items event: {event.items()}")
        photo = event.get('photo')
        bucket = event.get('bucket')
        if not photo:
            raise ValueError("'photo' is missing in the body")

        if not bucket:
            raise ValueError("'bucket' is missing in the body")

        text = detect_text(photo=photo, bucket=bucket)

        return {
            'statusCode': 200,
            'body': json.dumps(
                {'result': text}
            ),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
