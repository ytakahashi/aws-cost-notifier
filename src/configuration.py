#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml
from datetime import datetime

DEFAULT_CONF_PATH = f"{os.path.dirname(os.path.abspath(__file__))}/resource/default.yml"

ENV_KEY_WEBHOOK_URL = "SLACK_WEBHOOK_URL"

ENV_KEY_SLACK_ICON = "SLACK_ICON"
ENV_KEY_SLACK_CHANNEL = "SLACK_CHANNEL"
ENV_KEY_SLACK_BOT_NAME = "SLACK_BOT_NAME"

ENV_KEY_NOTIFY_THRESHOLD_GOOD = "NOTIFY_THRESHOLD_GOOD"
ENV_KEY_NOTIFY_THRESHOLD_WARN = "NOTIFY_THRESHOLD_WARN"


class Configuration:

    def __init__(self):
        self.__url = os.environ.get(ENV_KEY_WEBHOOK_URL)
        if self.__url is None:
            raise ValueError('SLACK_WEBHOOK_URL is not specified.')

        self.__icon = os.environ.get(ENV_KEY_SLACK_ICON)
        self.__channel = os.environ.get(ENV_KEY_SLACK_CHANNEL)
        self.__bot_name = os.environ.get(ENV_KEY_SLACK_BOT_NAME)

        self.__threshold_good = os.environ.get(ENV_KEY_NOTIFY_THRESHOLD_GOOD)
        self.__threshold_warn = os.environ.get(ENV_KEY_NOTIFY_THRESHOLD_WARN)

        self.__called_date = datetime.utcnow()

        with open(DEFAULT_CONF_PATH) as file:
            default_config = yaml.load(file)

        self.__slack_config = default_config["slack"]
        self.__cloudwatch_config = default_config["cloudwatch"]

    @property
    def url(self):
        pass

    @url.getter
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        raise ValueError('This value cannot be updated.')

    @property
    def icon(self):
        if self.__icon is None:
            return self.__slack_config.get("icon")
        else:
            return self.__icon

    @icon.setter
    def icon(self, value):
        raise ValueError('This value cannot be updated.')

    @property
    def channel(self):
        return self.__channel

    @channel.setter
    def channel(self, value):
        raise ValueError('This value cannot be updated.')

    @property
    def bot_name(self):
        if self.__bot_name is None:
            return self.__slack_config.get("bot_name")
        else:
            return self.__bot_name

    @bot_name.setter
    def bot_name(self, value):
        raise ValueError('This value cannot be updated.')

    @property
    def threshold_good(self):
        if self.__threshold_good is None:
            return self.__cloudwatch_config.get("threshold_good")
        else:
            return float(self.__threshold_good)

    @threshold_good.setter
    def threshold_good(self, value):
        raise ValueError('This value cannot be updated.')

    @property
    def threshold_warn(self):
        if self.__threshold_warn is None:
            return self.__cloudwatch_config.get("threshold_warn")
        else:
            return float(self.__threshold_warn)

    @threshold_warn.setter
    def threshold_warn(self, value):
        raise ValueError('This value cannot be updated.')

    @property
    def called_date(self):
        return self.__called_date

    @called_date.setter
    def called_date(self, value):
        raise ValueError('This value cannot be updated.')

