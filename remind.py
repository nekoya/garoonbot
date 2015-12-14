import argparse
import datetime
import sys

from garoonbot import api, conf, fmt, schedule, slack


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', type=int, help='User id')
    parser.add_argument('-f', '--facility', type=int, help='Facility id')
    parser.add_argument('-c', '--channel', type=str, help='Slack channel')
    parser.add_argument('-n', '--username', type=str, help='Slack username')
    parser.add_argument('-e', '--emoji', type=str, help='Slack icon_emoji')
    parser.add_argument(
        '-d', '--datetime',
        type=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M'),
        help='Target datetime YYYY-mm-dd HH:MM')
    parser.set_defaults(datetime=datetime.datetime.now()+datetime.timedelta(minutes=10))

    args = parser.parse_args()
    f = lambda x: not any(x) or all(x)
    if f((args.user, args.facility)):
        parser.print_help()
        sys.exit(1)

    for key in ('username', 'emoji', 'channel'):
        if getattr(args, key):
            conf.settings['slack'][key] = getattr(args, key)

    if args.user:
        xml = api.get_user_schedule(date=args.datetime, user_id=args.user)
        with_facility = True
    else:
        xml = api.get_facility_schedule(date=args.datetime, facility_id=args.facility)
        with_facility = False

    events = [fmt.event(x, with_facility) for x in schedule.find_events(xml)
              if x.period[0] == fmt.hm(args.datetime)]
    if events:
        slack.send(u'10分後にイベントがあります', '\n\n'.join(events))
