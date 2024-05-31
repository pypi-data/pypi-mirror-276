import logging
import math
from django.db import transaction, connection

from common.table_util import TableUtil

logger = logging.getLogger(__name__)


class DataPurgingUtil:

    @classmethod
    def archive_and_purge_stale_data(cls, table_name_str, main_table_name, interval_type, db_record_size,
                                     table_name_prefix, all_fields, purge_function_name):
        interval_start_date, interval_end_date, archive_table_name = TableUtil.get_last_to_last_interval_dates_and_archive_table_name(
            interval_type, table_name_str, table_name_prefix)
        total_count = purge_function_name.get_count_of_records_between_interval_dates(interval_start_date,
                                                                                      interval_end_date,
                                                                                      main_table_name)
        if total_count > 0:
            loop_count = math.ceil(total_count / db_record_size)
            is_archive_table_present = False
            for _ in range(0, loop_count):
                all_fields_and_values, records_to_delete = purge_function_name.get_stale_records(main_table_name,
                                                                                                 interval_start_date,
                                                                                                 interval_end_date,
                                                                                                 all_fields,
                                                                                                 db_record_size)
                cursor = connection.cursor()

                with transaction.atomic():
                    if is_archive_table_present is False:
                        TableUtil.create_archive_table(archive_table_name, table_name_str, table_name_prefix,
                                                       cursor)
                        TableUtil.make_migrations_to_create_table()
                        is_archive_table_present = True
                    TableUtil.insert_data_to_new_archive_table(archive_table_name, all_fields_and_values, cursor)
                    logger.info("Records are successfully inserted in archive table {}".format(archive_table_name))
                    TableUtil.delete_records(table_name_str, records_to_delete, table_name_prefix, cursor)
                    logger.info("Records are successfully deleted from the main table {}".format(main_table_name))