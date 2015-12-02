import json

import requests

from garoonbot import schedule
from garoonbot.conf import settings


def send(message):
    requests.post(
        settings['slack']['url'],
        data=json.dumps({
            'username': settings['slack']['username'],
            'icon_emoji': settings['slack']['emoji'],
            'text': message,
            'channel': settings['slack']['channel']}),
        timeout=10)


def report_events(headline, events):
    send('```\n%s\n\n%s\n```' % (
        headline,
        '\n\n'.join([schedule.show(x) for x in events])))
