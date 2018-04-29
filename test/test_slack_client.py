#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest.mock import MagicMock, patch
from nose.tools import eq_
from src.slack_client import Slack


class TestSlack(TestCase):

    def test_test_send_message(self):
        url = "url"
        name = "name"
        icon = "icon"

        account_id = "123"
        date = "2018/04/01"
        cost = "10"
        color = "color"

        slack = Slack(url, icon, None, name)

        expected = {
            "username": f"{name}",
            "icon_emoji": f"{icon}",
            "attachments": [
                {
                    "title": f"Cost of AWS (account: {account_id})",
                    "text": f"{date} -> ${cost}",
                    "color": color,
                    "mrkdwn_in": ["text", "pretext"]
                }
            ]
        }

        actual = slack.create_payload(account_id, date, cost, color)

        eq_(expected, actual)

    def test_test_send_message_channel_not_noe(self):
        url = "url"
        channel = "channel"
        name = "name"
        icon = "icon"

        account_id = "123"
        date = "2018/04/01"
        cost = "10"
        color = "color"

        slack = Slack(url, icon, channel, name)

        expected = {
            "channel": "channel",
            "username": f"{name}",
            "icon_emoji": f"{icon}",
            "attachments": [
                {
                    "title": f"Cost of AWS (account: {account_id})",
                    "text": f"{date} -> ${cost}",
                    "color": color,
                    "mrkdwn_in": ["text", "pretext"]
                }
            ]
        }

        actual = slack.create_payload(account_id, date, cost, color)

        eq_(expected, actual)

    @patch('src.slack_client.SlackClient')
    def test_send_message(self, mock):
        url = "url"
        slack = Slack(url, None, None, None)

        slack.send_message({"foo": "bar"})

        mock.assert_called_with(url)
