#!/usr/bin/env python3

import boto3
import os
import json


aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']


def _rule_create(_event, _context):
    rule_name = "test"
    cloudwatch_events = boto3.client('events', aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
    put_rule_response = cloudwatch_events.put_rule(
        Name=rule_name,
        ScheduleExpression='rate(30 minutes)',
        State='ENABLED'
    )
    put_targets_response = cloudwatch_events.put_targets(
        Rule=rule_name,
        Targets=[
            {
                'Arn': 'arn:aws:lambda:us-east-1:653057332392:function:dev-queuePush',
                'Id': 'myCloudWatchEventsTarget',
            },
        ]
    )
    return {'statusCode': 201,
            'body': json.dumps(put_targets_response)}

