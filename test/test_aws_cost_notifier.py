#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from nose.tools import eq_, raises
from datetime import datetime
from src import aws_cost_notifier as sut


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
