#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest.mock import MagicMock
from src import aws_cost_notifier as sut


class TestNotificationColor(TestCase):

    def test_notification_color_good(self):
        actual = sut.notification_color(0.0)

        print(actual)
        assert actual == "good"

    def test_notification_color_warning(self):
        actual = sut.notification_color(0.5)

        print(actual)
        assert actual == "warning"

    def test_notification_color_danger(self):
        actual = sut.notification_color(5.0)

        print(actual)
        assert actual == "danger"


class TestGetAccountId(TestCase):

    def test_get_account_id(self):
        mock_resp = MagicMock()
        mock_resp.get.return_value = "1234"

        mock_client = MagicMock()
        mock_client.get_caller_identity.return_value = mock_resp

        res = sut.get_account_id(mock_client)
        assert res == "1234"

        mock_client.get_caller_identity.assert_called_once()

