#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest.mock import MagicMock, patch
from nose.tools import eq_, raises
from datetime import datetime
from src import aws_cost_notifier as sut


class TestLambdaHandler(TestCase):

    def test_normal_lambda_handler(self):
        with patch('src.aws_cost_notifier.boto3'):
            sut.get_metric_statistics = MagicMock()
            sut.handle_cloudwatch_response = MagicMock(return_value=("2018/04/01", 0.0))
            sut.get_account_id = MagicMock(return_value=23456)
            sut.send_message = MagicMock()

            sut.lambda_handler(None, None)

            sut.get_metric_statistics.assert_called_once()
            sut.handle_cloudwatch_response.assert_called_once()
            sut.get_account_id.assert_called_once()
            sut.send_message.assert_called_once()


class TestHandleCloudwatchResponse(TestCase):

    def test_normal_sort_list(self):
        statistics = [
            {
                'Timestamp': datetime.strptime('2018/04/01', '%Y/%m/%d'),
                'Maximum': 1.0
            },
            {
                'Timestamp': datetime.strptime('2018/05/01', '%Y/%m/%d'),
                'Maximum': 2.0
            },
            {
                'Timestamp': datetime.strptime('2018/03/01', '%Y/%m/%d'),
                'Maximum': 3.0
            }
        ]

        cost, date = sut.handle_cloudwatch_response({'Datapoints': statistics})

        eq_(cost, 2.0)
        eq_(date, "2018/05/01")

    @raises(ValueError)
    def test_error_empty_statistics(self):
        statistics = []

        sut.handle_cloudwatch_response({'Datapoints': statistics})


class TestGetAccountId(TestCase):

    def test_get_account_id(self):
        mock_resp = MagicMock()
        mock_resp.get.return_value = "1234"

        mock_client = MagicMock()
        mock_client.get_caller_identity.return_value = mock_resp

        res = sut.get_account_id(mock_client)

        eq_(res, "1234")

        mock_client.get_caller_identity.assert_called_once()


class TestNotificationColor(TestCase):

    def test_notification_color_good(self):
        actual = sut.notification_color(0.0)

        eq_(actual, "good")

    def test_notification_color_warning(self):
        actual = sut.notification_color(0.5)

        eq_(actual, "warning")

    def test_notification_color_danger(self):
        actual = sut.notification_color(5.0)

        eq_(actual, "danger")


class TestGetMetricStatistics(TestCase):

    def test_get_metric_statistics(self):
        mock_client = MagicMock()

        sut.get_metric_statistics(mock_client)

        mock_client.get_metric_statistics.assert_called_once()
