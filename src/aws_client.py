#!/usr/bin/env python
# -*- coding: utf-8 -*-

import boto3
from datetime import timedelta


class StsClient:

    def __init__(self):
        self.client = boto3.client('sts')

    def get_account_id(self):
        caller_identity = self.client.get_caller_identity()
        return caller_identity.get("Account")


class CloudwatchClient:

    def __init__(self):
        self.client = boto3.client('cloudwatch', region_name='us-east-1')

    def get_metric_statistics(self, date):
        metric_statistics_response = self.client.get_metric_statistics(
            Namespace='AWS/Billing',
            MetricName='EstimatedCharges',
            Dimensions=[
                {
                    'Name': 'Currency',
                    'Value': 'USD'
                }
            ],
            StartTime=date - timedelta(days=1),
            EndTime=date,
            Period=86400,
            Statistics=['Maximum']
        )
        return metric_statistics_response

