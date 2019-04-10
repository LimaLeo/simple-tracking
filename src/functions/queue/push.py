#!/usr/bin/env python3

import boto3
import os
import json

aws_access_key_id_local = os.environ['AWS_ACCESS_KEY_ID_LOCAL']
aws_secret_access_key_local = os.environ['AWS_SECRET_ACCESS_KEY_LOCAL']

def push(_event, _context):
    sqs = boto3.client('sqs', aws_access_key_id=aws_access_key_id_local,aws_secret_access_key=aws_secret_access_key_local)
    response = sqs.create_queue(
        QueueName='SQS_QUEUE_NAME',
        Attributes={
            'DelaySeconds': '10',
            'MessageRetentionPeriod': '86400'
        }
    )
    return {'statusCode': 201,
            'body': json.dumps(response)}
