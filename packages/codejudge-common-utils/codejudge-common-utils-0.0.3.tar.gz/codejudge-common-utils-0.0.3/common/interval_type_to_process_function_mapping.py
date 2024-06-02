from common.interval_dates_and_archive_table_name import MonthlyArchiveTableInterval, QuarterlyArchiveTableInterval, \
    YearlyArchiveTableInterval

from common.enums import IntervalType


interval_type_to_process_function_mapping = {
    IntervalType.MONTHLY.value: MonthlyArchiveTableInterval(),
    IntervalType.QUARTERLY.value: QuarterlyArchiveTableInterval(),
    IntervalType.YEARLY.value: YearlyArchiveTableInterval(),
}