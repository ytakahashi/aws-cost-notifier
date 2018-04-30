#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest.mock import MagicMock, patch
from nose.tools import eq_
from src.aws_client import StsClient
from src.aws_client import CloudwatchClient
from datetime import datetime


class TestSts(TestCase):

    def test_get3(self):
        test_client = TestClient()
        mock_client = MagicMock(return_value=test_client)

        with patch('src.aws_client.boto3.client', mock_client):
            sts_client = StsClient()

            res = sts_client.get_account_id()

            eq_(res, "1234")


class TestCloudwatch(TestCase):

    def test_get_metric_statistics(self):
        test_client = TestClient()
        mock_client = MagicMock(return_value=test_client)
        with patch('src.aws_client.boto3.client', mock_client):
            cw_client = CloudwatchClient()

            res = cw_client.get_metric_statistics(datetime.utcnow())

            eq_(res, {"foo": "bar"})


class TestClient:

    def get_caller_identity(self):
        return {"Account": "1234"}

    def get_metric_statistics(self, **kwargs):
        return {"foo": "bar"}
