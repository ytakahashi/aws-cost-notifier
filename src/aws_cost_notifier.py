#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from aws_client import CloudwatchClient
from aws_client import StsClient
from slack_client import Slack
from configuration import Configuration


def lambda_handler(event, context):
    cloudwatch = CloudwatchClient()
    sts = StsClient()
    conf = Configuration()

    metric_statistics_response = cloudwatch.get_metric_statistics(conf.called_date)

    cost, date = handle_cloudwatch_response(metric_statistics_response)

    caller_account = sts.get_account_id()

    slack = Slack(conf.url, conf.icon, conf.channel, conf.bot_name)
    payload = slack.create_payload(caller_account, date, cost)

    slack.send_message(payload)


def handle_cloudwatch_response(metric_statistics_response):
    statistics = metric_statistics_response['Datapoints']

    if not statistics:
        raise ValueError("Could not fetch cloudwatch metric statistics")

    sorted_statistics = sorted(statistics, key=lambda s: s['Timestamp'], reverse=True)

    cost = sorted_statistics[0]['Maximum']
    date = sorted_statistics[0]['Timestamp'].strftime('%Y/%m/%d')

    return cost, date


if __name__ == "__main__":
    lambda_handler(None, None)
