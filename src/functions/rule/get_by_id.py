#!/usr/bin/env python3

import boto3
import os
import json


def get_by_id(_event, _context):
    client = boto3.client('events')
    response = client.list_rules(NamePrefix='test')
    return {'statusCode': 201,
            'body': json.dumps(response)}
