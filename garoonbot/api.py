import ssl

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

from garoonbot.conf import settings


tmpl = '''<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
  <soap:Header>
    <Action>%(action)s</Action>
    <Security>
      <UsernameToken>
        <Username>%(user)s</Username>
        <Password>%(password)s</Password>
      </UsernameToken>
    </Security>
    <Timestamp>
      <Created>2010-08-12T14:45:00Z</Created>
      <Expires>2037-08-12T14:45:00Z</Expires>
    </Timestamp>
    <Locale>jp</Locale>
  </soap:Header>
  <soap:Body>
    <%(action)s>
      <parameters start="%(date)sT00:00:00" end="%(date)sT14:59:59">%(params)s</parameters>
    </%(action)s>
  </soap:Body>
</soap:Envelope>
'''


class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)


def _get_schedule(date, params):
    s = requests.Session()
    s.mount('https://', TLSAdapter(max_retries=5))
    return s.post(
        settings['garoon']['url'],
        data=tmpl % {'action': 'ScheduleGetEventsByTarget',
                     'user': settings['garoon']['user'],
                     'password': settings['garoon']['password'],
                     'date': date.strftime('%Y-%m-%d'),
                     'params': params},
        **settings['garoon'].get('options', {})).text


def get_user_schedule(date, user_id):
    return _get_schedule(date, '<user id="%d"></user>' % user_id)


def get_facility_schedule(date, facility_id):
    return _get_schedule(date, '<facility id="%d"></facility>' % facility_id)
