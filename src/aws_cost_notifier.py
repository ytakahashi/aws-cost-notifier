#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import boto3
from slackweb import slackweb
from datetime import datetime, timedelta

CURRENT_DATE = datetime.utcnow()
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")


def lambda_handler(event, context):
    cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
    sts = boto3.client('sts')

    metric_statistics_response = get_metric_statistics(cloudwatch)

    cost, date = handle_cloudwatch_response(metric_statistics_response)

    caller_account = get_account_id(sts)

    send_message(caller_account, date, cost)


def handle_cloudwatch_response(metric_statistics_response):
    statistics = metric_statistics_response['Datapoints']

    if not statistics:
        raise ValueError("Could not fetch cloudwatch metric statistics")

    sorted_statistics = sorted(statistics, key=lambda s: s['Timestamp'], reverse=True)

    cost = sorted_statistics[0]['Maximum']
    date = sorted_statistics[0]['Timestamp'].strftime('%Y/%m/%d')

    return cost, date


def get_account_id(client):
    caller_identity = client.get_caller_identity()
    return caller_identity.get("Account")


def send_message(account_id, date, cost):
    attachment = {"title": f"Cost of AWS (account: {account_id})",
                  "text": f"{date} -> ${cost}",
                  "color": notification_color(cost),
                  "mrkdwn_in": ["text", "pretext"]}

    attachments = [attachment]
    slack = slackweb.Slack(url=SLACK_WEBHOOK_URL)
    slack.notify(attachments=attachments)


def notification_color(cost):
    if cost <= 0.0:
        return "good"
    elif cost <= 1.0:
        return "warning"
    else:
        return "danger"


def get_metric_statistics(client):
    metric_statistics_response = client.get_metric_statistics(
        Namespace='AWS/Billing',
        MetricName='EstimatedCharges',
        Dimensions=[
            {
                'Name': 'Currency',
                'Value': 'USD'
            }
        ],
        StartTime=CURRENT_DATE - timedelta(days=1),
        EndTime=CURRENT_DATE,
        Period=86400,
        Statistics=['Maximum'])
    return metric_statistics_response


if __name__ == "__main__":
    lambda_handler(None, None)
