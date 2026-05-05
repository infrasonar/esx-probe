import calendar
import datetime


def datetime_to_timestamp(inp: datetime.datetime | None) -> int | None:
    if inp is None:
        return inp
    return calendar.timegm(inp.timetuple())
