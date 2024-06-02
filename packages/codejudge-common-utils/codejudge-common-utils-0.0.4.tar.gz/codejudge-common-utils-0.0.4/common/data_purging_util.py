import logging
import math
import os.path

from django.db import transaction, connection
from rest_framework import status

from common.constants import DATA_PURGING_MAX_RETRY
from common.table_util import TableUtil
from restapi.common.list_util import ListUtil
from restapi.common.file_util import FileUtil
from restapi.test.worker.data_purging_framework.data_purging_process import get_unique_ids_to_s3_file_paths_map, \
    upload_json_file_in_s3_and_get_uuid_to_file_urls_map
from restapi.exception.exception import RecruitException


logger = logging.getLogger(__name__)


class DataPurgingUtil:

    @classmethod
    def archive_and_purge_stale_data(cls, table_name_str, main_table_name, interval_type, db_record_size,
                                     table_name_prefix, all_fields, purge_function_name, filter_table_name, app1,
                                     is_fb):
        workspaces = []
        is_archive_table_present = False
        is_completed = False
        archive_table_name = None
        all_fields_and_values = None
        records_to_delete = None
        try:
            interval_start_date, interval_end_date, archive_table_name = TableUtil.get_last_to_last_interval_dates_and_archive_table_name(
                interval_type, table_name_str, table_name_prefix)
            if is_fb:
                main_table_name = filter_table_name
            total_count = purge_function_name.get_count_of_records_between_interval_dates(interval_start_date,
                                                                                          interval_end_date,
                                                                                          main_table_name)
            if total_count > 0:
                loop_count = math.ceil(total_count / db_record_size)
                for _ in range(0, loop_count):
                    all_fields_and_values, records_to_delete = purge_function_name.get_stale_records(main_table_name,
                                                                                                     interval_start_date,
                                                                                                     interval_end_date,
                                                                                                     all_fields,
                                                                                                     table_name_str,
                                                                                                     db_record_size,
                                                                                                     app1)
                    if is_fb:
                        unique_ids_to_s3_file_paths_map, unique_ids_to_file_names_map, workspaces = get_unique_ids_to_s3_file_paths_map(
                            records_to_delete)
                        uuid_to_file_urls_map = upload_json_file_in_s3_and_get_uuid_to_file_urls_map(
                            unique_ids_to_s3_file_paths_map, unique_ids_to_file_names_map)
                        all_fields_and_values = [uuid_to_file_urls_map]
                    cursor = connection.cursor()

                    with transaction.atomic():
                        if is_archive_table_present is False:
                            TableUtil.drop_archive_table_if_exist(archive_table_name, cursor)
                            TableUtil.create_archive_table(archive_table_name, table_name_str, table_name_prefix,
                                                           cursor, is_fb)
                            TableUtil.make_migrations_to_create_table()
                            is_archive_table_present = True
                        TableUtil.insert_data_to_new_archive_table(archive_table_name, all_fields_and_values, cursor)
                        logger.info("Records are successfully inserted in archive table {}".format(archive_table_name))
                        TableUtil.delete_records(table_name_str, records_to_delete, table_name_prefix, cursor, is_fb,
                                                 app1)
                        logger.info("Records are successfully deleted from the main table {}".format(main_table_name))
                        is_completed = True
        except Exception as e:
            if is_completed is False:
                retry_count = DATA_PURGING_MAX_RETRY
                while retry_count > 0:
                    cursor = connection.cursor()
                    with transaction.atomic():
                        if is_archive_table_present is False:
                            TableUtil.drop_archive_table_if_exist(archive_table_name)
                            TableUtil.create_archive_table(archive_table_name, table_name_str, table_name_prefix, cursor, is_fb)
                            TableUtil.make_migrations_to_create_table()
                            is_archive_table_present = True
                        TableUtil.insert_data_to_new_archive_table(archive_table_name, all_fields_and_values, cursor)
                        logger.info("Records are successfully inserted in archive table {}".format(archive_table_name))
                        TableUtil.delete_records(table_name_str, records_to_delete, table_name_prefix, cursor, is_fb,
                                                 app1)
                        logger.info("Records are successfully deleted from the main table {}".format(main_table_name))
                        is_completed = True
                    if is_completed is False:
                        retry_count = retry_count - 1
                        if retry_count == 0:
                            raise RecruitException(
                                "Couldn't create table or insert rows in the table name {}, Please check the error: {}!".format(
                                    archive_table_name, str(e)), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:
                        break

        finally:
            if ListUtil.is_valid(workspaces):
                for workspace in workspaces:
                    if workspace is not None and os.path.exists(workspace):
                        FileUtil.delete_folder(workspace, False)