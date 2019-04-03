#!/usr/bin/env python3

import boto3
import os
import json


aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']


def _rule_create(_event, _context):
    client = boto3.client('events', aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
    response = client.put_rule(
        Name='test3',
        ScheduleExpression='rate(5 minutes)',
        State='ENABLED'
    )
    return {'statusCode': 201,
            'body': json.dumps(response)}

