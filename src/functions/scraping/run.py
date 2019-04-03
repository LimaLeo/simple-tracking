#!/usr/bin/env python3

import boto3


def run(_event, _context):
    return {'statusCode': 201,
            'body': "test"}
