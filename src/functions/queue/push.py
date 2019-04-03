#!/usr/bin/env python3

import boto3


aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']


def push(_event, _context):
    client = boto3.client('events', aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)

    response = client.list_rules(NamePrefix='test')

    print(response)
    return {'statusCode': 201,
            'body': "test"}
