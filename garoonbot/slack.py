import json

import requests

from garoonbot import schedule
from garoonbot.conf import settings


def send(message):
    requests.post(
        settings['slack']['url'],
        data=json.dumps({
            'username': settings['slack']['username'],
            'icon_emoji': ':%s:' % settings['slack']['emoji'].strip(':'),
            'text': message,
            'channel': settings['slack']['channel']}),
        timeout=10)


def report_events(headline, events):
    message = '\n\n'.join([schedule.show(x) for x in events])
    if not events:
        message = u'＿人人人人人人＿\n＞　予定なし　＜\n￣Y^Y^Y^Y^Y￣'
    send('```\n%s\n\n%s\n```' % (
        headline, message))
