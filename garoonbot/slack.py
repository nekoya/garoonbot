import json

import requests

from garoonbot import schedule
from garoonbot.conf import settings


def send(headline, events):
    message = '```\n%s\n\n%s\n```' % (
        headline,
        '\n\n'.join([schedule.show(x) for x in events]))
    requests.post(
        settings['slack']['url'],
        data=json.dumps({
            'username': 'schedulebot',
            'icon_emoji': ':date:',
            'text': message,
            'channel': settings['slack']['channel']}),
        timeout=10)
