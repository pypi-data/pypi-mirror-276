import calendar
import time
from datetime import datetime, timedelta
from math import floor

import pytz
from django.utils import timezone


class DateTimeUtil:

    @classmethod
    def current_millis(cls):
        return int(round(time.time() * 1000))

    @classmethod
    def current_seconds(cls):
        return int(round(time.time()))

    @classmethod
    def current_time(cls):
        return timezone.now().replace(microsecond=0)

    @classmethod
    def current_date(cls):
        return cls.current_time().date()

    @classmethod
    def current_year(cls):
        return cls.current_time().year

    @classmethod
    def remove_microsecond(cls, inp_time):
        if inp_time:
            return inp_time.replace(microsecond=0)
        return inp_time

    @classmethod
    def transform_to_string(cls, dt_time_obj, to_tz_suffix='UTC'):
        if dt_time_obj and type(dt_time_obj) is datetime:
            to_tz_suffix = to_tz_suffix if to_tz_suffix != 'UTC' else to_tz_suffix + '%z'
            return dt_time_obj.strftime("%b %d, %Y, %H:%M %p " + to_tz_suffix)
        return dt_time_obj

    @classmethod
    def transform_datetime_with_tz(cls, inp_time, to_tz_str='UTC'):
        inp_time = inp_time.replace(tzinfo=pytz.UTC)
        time_zone_str = to_tz_str if to_tz_str is not None else 'UTC'
        to_time = inp_time.astimezone(pytz.timezone(time_zone_str))
        return cls.transform_to_string(to_time, to_time.tzname())

    @classmethod
    def transform_to_db_time_str(cls, time_obj, time_format=None):
        if time_format is None:
            time_format = '%Y-%m-%d %H:%M:%S'
        return time_obj.strftime(time_format)

    @classmethod
    def get_timestamp_from_datetime(cls, dt, tz_info=timezone.utc):
        if dt:
            return dt.replace(tzinfo=tz_info).timestamp()
        return dt

    @classmethod
    def convert_iso_string_to_db_time_obj(cls, inp_time):
        naive_time = datetime.strptime(inp_time, "%Y-%m-%dT%H:%M:%SZ")
        return pytz.timezone('UTC').localize(naive_time)

    @classmethod
    def convert_string_to_db_time_obj(cls, inp_time):
        naive_time = datetime.strptime(inp_time, "%Y-%m-%d %H:%M:%S")
        return pytz.timezone('UTC').localize(naive_time)

    @classmethod
    def convert_iso_string_to_db_time_obj_with_milliseconds(cls, inp_time):
        naive_time = datetime.strptime(inp_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        return pytz.timezone('UTC').localize(naive_time)

    @classmethod
    def append_timezone_to_db_time_str(cls, db_time_str, tz='Z'):
        return db_time_str + tz

    @classmethod
    def convert_naive_to_aware_time(cls, dt):
        return pytz.timezone('UTC').localize(dt)

    @classmethod
    def transform_to_seconds(cls, dt_time_obj):
        if dt_time_obj:
            return int(dt_time_obj.replace(tzinfo=pytz.utc).timestamp())
        return None

    @classmethod
    def transform_to_minutes(cls, seconds):
        if seconds is not None:
            return seconds // 60
        return None

    @classmethod
    def get_datetime_from_timestamp(cls, timestamp, user_timezone='UTC', to_str=False, time_format=None):
        if timestamp:
            user_timezone = 'UTC' if user_timezone is None else user_timezone
            transformed_time = datetime.fromtimestamp(timestamp, pytz.timezone(user_timezone))
            if to_str and to_str is True:
                transformed_time = cls.transform_to_db_time_str(transformed_time.replace(microsecond=0), time_format)
            return transformed_time
        return None

    @classmethod
    def convert_seconds_test_pdf(cls, seconds):
        if not isinstance(seconds, float) and not isinstance(seconds, int):
            return seconds

        if seconds is None or seconds == 0:
            return '0s'

        seconds = int(seconds)
        output = ''

        days = floor(seconds / (3600 * 24))
        output += cls.__append_to_time_test_pdf(days, 'd')

        seconds -= days * 3600 * 24
        hours = floor(seconds / 3600)
        output += cls.__append_to_time_test_pdf(hours, 'h')

        seconds -= hours * 3600
        minutes = floor(seconds / 60)
        output += cls.__append_to_time_test_pdf(minutes, 'm')

        seconds -= minutes * 60
        output += cls.__append_to_time_test_pdf(seconds, 's')

        return output.strip()

    @classmethod
    def convert_seconds(cls, seconds):
        if not isinstance(seconds, float) and not isinstance(seconds, int):
            return seconds

        if seconds is None or seconds == 0:
            return '0 s'

        seconds = int(seconds)
        output = ''

        days = floor(seconds / (3600 * 24))
        output += cls.__append_to_time(days, 'day' + cls.__append_if_plural(days))

        seconds -= days * 3600 * 24
        hours = floor(seconds / 3600)
        output += cls.__append_to_time(hours, 'hr' + cls.__append_if_plural(hours))

        seconds -= hours * 3600
        minutes = floor(seconds / 60)
        output += cls.__append_to_time(minutes, 'min' + cls.__append_if_plural(minutes))

        seconds -= minutes * 60
        output += cls.__append_to_time(seconds, 's')

        return output.strip()

    @classmethod
    def get_time_from_timing(cls, from_timezone, timing, to_timezone='UTC'):
        to_tz = pytz.timezone(to_timezone)
        from_tz = pytz.timezone(from_timezone)
        from_tz_now = datetime.now(from_tz)
        from_tz_timing_to_to_tz = from_tz_now.replace(hour=timing['hourOfDay'], minute=timing['minOfDay'],
                                                      second=timing['secOfDay']).astimezone(to_tz)
        return from_tz_timing_to_to_tz

    @classmethod
    def get_interval_start_date_and_end_date_for_quarterly(cls, year, last_to_last_quarter):
        interval_start_date = cls.transform_to_db_time_str(datetime(year, (last_to_last_quarter - 1) * 3 + 1, 1))
        if last_to_last_quarter == 4:
            year += 1
            last_to_last_quarter = 1
        else:
            last_to_last_quarter = last_to_last_quarter * 3 + 1
        interval_end_date = cls.transform_to_db_time_str(datetime(year, last_to_last_quarter, 1))
        return interval_start_date, interval_end_date

    @classmethod
    def get_interval_start_date_and_end_date_for_monthly(cls, year, last_to_last_month, current_date):
        interval_start_date = datetime(year, last_to_last_month, 1)  # Start of interval
        interval_end_date = datetime(year, last_to_last_month, current_date.day)
        return interval_start_date, interval_end_date

    @classmethod
    def get_interval_start_date_and_end_date_for_yearly(cls, last_to_last_year):
        interval_start_date = datetime(last_to_last_year, 1, 1)
        interval_end_date = datetime(last_to_last_year, 12, 31)
        return interval_start_date, interval_end_date

    @classmethod
    def transform_seconds_to_formatted_time(cls, total):
        mins = total // 60
        hours = mins // 60
        return "%02d:%02d:%02d" % (hours, mins % 60, total % 60)

    @classmethod
    def timedelta_from_current_time(cls, ch_dict):
        return datetime.utcnow() + timedelta(**ch_dict)

    @staticmethod
    def timedelta(time, ch_dict):
        return time + timedelta(**ch_dict)

    @classmethod
    def timedelta_to_current_time(cls, ch_dict):
        return cls.current_time() - timedelta(**ch_dict)

    @classmethod
    def check_if_dt_object_is_naive(cls, dt):
        return dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None

    @classmethod
    def __append_if_plural(cls, unit):
        if unit and unit > 1:
            return 's'
        return ''

    @classmethod
    def __append_to_time(cls, time, append_str):
        if time:
            return ' ' + str(time) + ' ' + append_str
        return ''

    @classmethod
    def __append_to_time_test_pdf(cls, time, append_str):
        if time:
            return ' ' + str(time) + append_str
        return ''

