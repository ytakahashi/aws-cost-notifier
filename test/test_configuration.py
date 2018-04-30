#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest.mock import MagicMock, patch
from nose.tools import eq_, raises
from src.configuration import Configuration
from datetime import datetime


class TestConfiguration(TestCase):

    def os_environ(*args):
        mock_env = {
            "SLACK_WEBHOOK_URL": "url",
            "SLACK_ICON": "icon",
            "SLACK_CHANNEL": "channel",
            "SLACK_BOT_NAME": "name",
            "NOTIFY_THRESHOLD_GOOD": "1",
            "NOTIFY_THRESHOLD_WARN": "2"
        }

        k = args[1]
        if k in mock_env:
            return mock_env[k]

    def os_environ_url_none(*args):
        mock_env = {
            "SLACK_ICON": "icon",
            "SLACK_CHANNEL": "channel",
            "SLACK_BOT_NAME": "name",
            "NOTIFY_THRESHOLD_GOOD": "1",
            "NOTIFY_THRESHOLD_WARN": "2"
        }

        k = args[1]
        if k in mock_env:
            return mock_env[k]

    def os_environ_url_only(*args):
        mock_env = {
            "SLACK_WEBHOOK_URL": "url",
        }

        k = args[1]
        if k in mock_env:
            return mock_env[k]

    @patch('src.configuration.datetime')
    @patch('src.configuration.os.environ.get')
    def test_normal(self, os_mock, date_mock):
        os_mock.side_effect = self.os_environ

        date_mock.utcnow.return_value = datetime(2018, 4, 21)

        conf = Configuration()

        eq_(conf.url, "url")
        eq_(conf.icon, "icon")
        eq_(conf.channel, "channel")
        eq_(conf.bot_name, "name")
        eq_(conf.threshold_good, 1)
        eq_(conf.threshold_warn, 2)
        eq_(conf.called_date, datetime(2018, 4, 21))

    @patch('src.configuration.datetime')
    @patch('src.configuration.os.environ.get')
    def test_normal_default(self, os_mock, date_mock):
        os_mock.side_effect = self.os_environ_url_only

        date_mock.utcnow.return_value = datetime(2018, 4, 21)

        conf = Configuration()

        eq_(conf.url, "url")
        eq_(conf.icon, ":moneybag:")
        eq_(conf.channel, None)
        eq_(conf.bot_name, "aws cost report")
        eq_(conf.threshold_good, 5.0)
        eq_(conf.threshold_warn, 15.0)
        eq_(conf.called_date, datetime(2018, 4, 21))

    @raises(ValueError)
    @patch('src.configuration.datetime')
    @patch('src.configuration.os.environ.get')
    def test_error_url(self, os_mock, date_mock):
        os_mock.side_effect = self.os_environ_url_none

        date_mock.utcnow.return_value = datetime(2018, 4, 21)

        Configuration()

