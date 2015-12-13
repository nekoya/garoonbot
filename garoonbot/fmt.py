# -*- coding: utf-8 -*-


def period(period):
    if len(period) == 2:
        return u'%s 〜 %s\n' % period
    return period[0]


def event(e):
    if e.facility:
        return '%s%s\n@%s' % (period(e.period), e.title, e.facility)
    return '%s%s' % (period(e.period), e.title)


def events(events):
    if not events:
        return u'＿人人人人人人＿\n＞　予定なし　＜\n￣Y^Y^Y^Y^Y￣'
    return '\n\n'.join([event(x) for x in events])


def date(dt):
    return dt.strftime('%Y-%m-%d %a')


def hm(dt):
    return dt.strftime('%H:%M')
