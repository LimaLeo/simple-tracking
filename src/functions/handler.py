#!/usr/bin/env python3

import boto3


def hello(_event, _context):
    client = boto3.client('events')

    response = client.list_rules(NamePrefix='test')

    print(response)
    return {'statusCode': 201,
            'body': "test"}
