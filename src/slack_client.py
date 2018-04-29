#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
import json
from urllib.request import urlopen
import logging
from logging import getLogger


class Slack:

    def __init__(self, url, icon, channel, name):
        self.url = url
        self.icon = icon
        self.channel = channel
        self.name = name

    def create_payload(self, account_id, date, cost, color):
        obj = {
            "username": f"{self.name}",
            "icon_emoji": f"{self.icon}",
            "attachments": [
                {
                    "title": f"Cost of AWS (account: {account_id})",
                    "text": f"{date} -> ${cost}",
                    "color": color,
                    "mrkdwn_in": ["text", "pretext"]
                }
            ]
        }

        if self.channel is not None:
            obj["channel"] = self.channel

        return obj

    def send_message(self, payload):
        client = SlackClient(self.url)
        client.send(payload)


class SlackClient:

    def __init__(self, url=""):
        self.url = url
        self.method = "POST"
        self.headers = {"Content-Type": "application/json"}

    def send(self, json_data):
        return self.request(json.dumps(json_data).encode("utf-8"))

    def request(self, json_data):
        request = urllib.request.Request(
            self.url,
            data=json_data,
            method=self.method,
            headers=self.headers
        )

        with urlopen(request) as response:
            response_body = response.read().decode("utf-8")
            logger = getLogger(__name__)
            logger.setLevel(logging.INFO)
            logger.info(f"Slack Response: {response_body}")

