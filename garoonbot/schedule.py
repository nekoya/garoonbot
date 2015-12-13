import datetime
from collections import namedtuple

from lxml import etree

Event = namedtuple('Event',  ('title',  'period', 'facility'))


def find_events(xml):
    _xml = etree.fromstring(xml.encode('utf-8'))
    return [eventify(x) for x in _xml.xpath('//schedule_event')]


def parse_period(event):
    elm = event.xpath('.//*[local-name()="date"]')
    if elm:
        return (u'終日 : ',)

    elm = event.xpath('.//*[local-name()="datetime"]')
    if elm:
        return (parse_jst_time(elm[0].attrib.get('start')),
                parse_jst_time(elm[0].attrib.get('end')))

    elm = event.xpath('.//*[local-name()="condition"]')
    if elm:
        return (elm[0].attrib.get('start_time')[:-3],
                elm[0].attrib.get('end_time')[:-3])
    return ('',)


def parse_jst_time(utc_datetime):
    if not utc_datetime:
        return ''
    return (datetime.datetime.strptime(utc_datetime, '%Y-%m-%dT%H:%M:%SZ') +
            datetime.timedelta(hours=9)).strftime('%H:%M')


def get_facility(event):
    elm = event.xpath('.//*[local-name()="facility"]')
    if elm:
        return elm[0].attrib['name']
    return ''


def eventify(node):
    return Event(
        ('%s %s' % (
            node.attrib.get('plan', ''),
            node.attrib.get('detail', ''))).strip(),
        parse_period(node),
        get_facility(node))
