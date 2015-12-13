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
        '-d', '--date',
        type=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'),
        help='Target date YYYY-mm-dd')
    parser.set_defaults(date=datetime.datetime.now())

    args = parser.parse_args()
    f = lambda x: not any(x) or all(x)
    if f((args.user, args.facility)):
        parser.print_help()
        sys.exit(1)

    for key in ('username', 'emoji', 'channel'):
        if getattr(args, key):
            conf.settings['slack'][key] = getattr(args, key)

    if args.user:
        xml = api.get_user_schedule(date=args.date, user_id=args.user)
    else:
        xml = api.get_facility_schedule(date=args.date, facility_id=args.facility)

    slack.send(fmt.date(args.date),
               fmt.events(schedule.find_events(xml)))
