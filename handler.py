import json
import os
import uuid

from jeffy.framework import get_app
from jeffy.sdk.kinesis import Kinesis
from jeffy.sdk.s3 import S3
from jeffy.sdk.sns import Sns
from jeffy.sdk.sqs import Sqs

import boto3
import requests

app = get_app()


@app.handlers.common()
def start_test(event, context):
    requests.post(
        os.environ['API_URL'],
        data=json.dumps({'foo': 'bar'}),
        headers={'content-type': 'application/json'})
    Sns().publish(
        topic_arn=os.environ['TOPIC_ARN'],
        subject='foo',
        message='bar')
    Kinesis().put_record(
        stream_name=os.environ['STREAM_NAME'],
        data={'foo': 'bar'},
        partition_key='partition_key')
    Sqs().send_message(
        queue_url=os.environ['QUEUE_URL'],
        message='hello world')
    S3().upload_file(
        file_path='logo.png', 
        bucket_name=os.environ['BUCKET_NAME'],
        key='logo.png')
    boto3.resource('dynamodb').Table(os.environ['TABLE_NAME']).put_item(Item={'id': str(uuid.uuid4())})
    return 'ok'


@app.handlers.rest_api()
def rest_api_test(event, context):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'result': 'ok.'})}


@app.handlers.sqs()
def sqs_test(event, context):
    return event


@app.handlers.sns()
def sns_test(event, context):
    return event


@app.handlers.kinesis_streams()
def kinesis_test(event, context):
    return event


@app.handlers.dynamodb_streams()
def dynamodb_test(event, context):
    return event


@app.handlers.s3()
def s3_test(event, context):
    del event['body']
    return event
