from datetime import date, datetime, timezone, timedelta

UTC = timezone(timedelta(hours=0))


def datetime_to_seconds(d):
    return int(d.timestamp())


def datetime_to_milliseconds(d):
    return int(d.timestamp()*1000)


def parse_date(date_str=None, shift=0):
    # return today if no date is provided
    if date_str is None:
        return date.today() - timedelta(days=shift)

    # parse provided string otherwise, and cast it to a date
    converted = datetime.strptime(date_str, "%Y-%m-%d").date()
    return converted - timedelta(days=shift)


def build_time_range(from_str=None, to_str=None, ago=1):
    """ This function expect human-formatted user input with a combination of
        - end date, e.g.: 2018-09-21   (default is today)
        - start date, e.g.: 2018-09-01 (default is today - nb of days ago)
        - number of days ago, e.g.: 30 (default is DEFAULT_NB_DAYS_AGO)
    """
    # validate dates
    end_date = parse_date(to_str)
    if from_str is None:
        start_date = end_date - timedelta(ago)
    else:
        start_date = parse_date(from_str)

    # make sure start is before end date
    if start_date > end_date:
        raise ValueError("Please provide a starting date before the end date")

    # convert dates to datetimes
    start_time = datetime.combine(start_date, datetime.min.time())
    end_time = datetime.combine(end_date, datetime.max.time())

    return start_time, end_time
