from abc import ABC, abstractmethod

from common.date_time_util import DateTimeUtil


class IntervalDatesAndArchiveTableNameInterface(ABC):

    @abstractmethod
    def get_interval_dates_and_archive_table_name(self, current_date, table_name_str, table_name_prefix):
        pass


class QuarterlyArchiveTableInterval(IntervalDatesAndArchiveTableNameInterface):

    def get_interval_dates_and_archive_table_name(self, current_date, table_name_str, table_name_prefix):
        current_quarter = (current_date.month - 1) // 3 + 1
        last_to_last_quarter = current_quarter - 2 if current_quarter > 1 else current_quarter + 2
        year = current_date.year - 1 if current_quarter <= 2 else current_date.year
        if last_to_last_quarter == 0:
            last_to_last_quarter = 4
        archive_table_name = table_name_prefix + "{}_q{}_{}".format(table_name_str.lower(), last_to_last_quarter, year)

        interval_start_date, interval_end_date = DateTimeUtil.get_interval_start_date_and_end_date_for_quarterly(year,
                                                                                                                 last_to_last_quarter)

        return interval_start_date, interval_end_date, archive_table_name


class MonthlyArchiveTableInterval(IntervalDatesAndArchiveTableNameInterface):

    def get_interval_dates_and_archive_table_name(self, current_date, table_name_str, table_name_prefix):
        # last_to_last_month = current_date.month - 2 if current_date.month > 1 else 12
        # year = current_date.year if current_date.month > 1 else current_date.year - 1
        # archive_table_name = "restapi_{}_m{}_{}".format(table_name_str.lower(), last_to_last_month, year)
        #
        # interval_start_date, interval_end_date = DateTimeUtil.get_interval_start_date_and_end_date_for_monthly(year,
        #                                                                                                        last_to_last_month,
        #                                                                                                        current_date)
        # return interval_start_date, interval_end_date, archive_table_name
        pass


class YearlyArchiveTableInterval(IntervalDatesAndArchiveTableNameInterface):

    def get_interval_dates_and_archive_table_name(self, current_date, table_name_str, table_name_prefix):
        # last_to_last_year = current_date.year - 2
        #
        # archive_table_name = "restapi_{}_{}".format(table_name_str.lower(), last_to_last_year)
        #
        # interval_start_date, interval_end_date = DateTimeUtil.get_interval_start_date_and_end_date_for_yearly(last_to_last_year)
        # return interval_start_date, interval_end_date, archive_table_name
        pass


