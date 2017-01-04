# -*- coding: utf-8 -*-


def period(period):
    """
    Args:
        period (tuple|str):

    Returns:
        str:
    """
    if isinstance(period, tuple):
        return u'{0:%H:%M} 〜 {1:%H:%M}\n'.format(period)
    return period


def event(e, with_facility=True):
    """
    Args:
        period (tuple):

    Returns:
        str:
    """
    if with_facility and e.facility:
        return '%s%s\n@%s' % (period(e.period), e.title, e.facility)
    return '%s%s' % (period(e.period), e.title)


def events(events, with_facility=True):
    """
    Args:
        events (list[Event]):
        with_facility (Optional[bool]):

    Returns:
        str:
    """
    if not events:
        return u'＿人人人人人人＿\n＞　予定なし　＜\n￣Y^Y^Y^Y^Y￣'
    return '\n\n'.join([event(x, with_facility) for x in events])


def date(dt):
    """
    Args:
        dt (datetime.datetime):

    Returns:
        str:
    """
    return dt.strftime('%Y-%m-%d %a')


def hm(dt):
    """
    Args:
        dt (datetime.datetime):

    Returns:
        str:
    """
    return dt.strftime('%H:%M')
