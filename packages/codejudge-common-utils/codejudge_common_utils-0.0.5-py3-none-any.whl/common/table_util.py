import logging
import re

from common.common_util import CommonUtil
from common.date_time_util import DateTimeUtil
from common.interval_type_to_process_function_mapping import interval_type_to_process_function_mapping
from firebase_admin import db

logger = logging.getLogger(__name__)


class TableUtil:
    @classmethod
    def get_last_to_last_interval_dates_and_archive_table_name(cls, interval_type, table_name_str, table_name_prefix):
        logger.info("Get last to last interval dates of interval type {} for table {}".format(interval_type, table_name_str))
        current_date = DateTimeUtil.current_date()
        return interval_type_to_process_function_mapping[interval_type].get_interval_dates_and_archive_table_name(current_date, table_name_str, table_name_prefix)

    @classmethod
    def create_archive_table(cls, archive_table_name, table_name_str, table_name_prefix, cursor, is_fb):
        logger.info("Creating archive table with name {}".format(archive_table_name))
        create_table_query = cls.get_create_table_query(table_name_str, table_name_prefix, cursor)
        archive_table_create_query = create_table_query[1].replace(create_table_query[0], archive_table_name)
        modified_archive_table_query = cls.modify_sql_query(archive_table_create_query, is_fb)
        drop_table_query = "DROP TABLE IF EXISTS {};"
        cursor.execute(modified_archive_table_query)

    @classmethod
    def drop_archive_table_if_exist(cls, archive_table_name, cursor):
        logger.info("Deleting archive table with name {} if exists".format(archive_table_name))
        drop_table_query = "DROP TABLE IF EXISTS {};".format(archive_table_name)
        cursor.execute(drop_table_query)

    @classmethod
    def modify_sql_query(cls, sql_query, is_fb):
        # Remove AUTO_INCREMENT from the entire query

        # Remove UNIQUE KEY, CONSTRAINT, and FOREIGN KEY lines
        sql_query_lines = sql_query.split('\n')
        sql_query_lines = [line for line in sql_query_lines if
                           not re.search(r'\b(UNIQUE KEY|CONSTRAINT|FOREIGN KEY)\b', line, re.IGNORECASE)]

        # Remove AUTO_INCREMENT value from the ENGINE line if it exists
        if is_fb is False:
            pattern = r'\bAUTO_INCREMENT\b|\b=\d+\b'
            # Replace the pattern with an empty string in each line of sql_query_lines
            sql_query_lines = [re.sub(pattern, '', line, flags=re.IGNORECASE) for line in sql_query_lines]

        # Clean up multiple spaces and commas
        modified_sql_query = '\n'.join(sql_query_lines).strip()
        modified_sql_query = re.sub(r'\s*,\s*', ', ', modified_sql_query)
        modified_sql_query = re.sub(r',\s*\)', ')', modified_sql_query)# Clean up commas
        modified_sql_query = re.sub(r'\s+', ' ', modified_sql_query)  # Clean up extra spaces

        return modified_sql_query

    @classmethod
    def get_create_table_query(cls, table_name_str, table_name_prefix, cursor):
        cursor.execute("SHOW CREATE TABLE " + table_name_prefix + "{};".format(table_name_str.lower()))
        result = cursor.fetchone()
        if result:
            return result
        else:
            return None

    @classmethod
    def make_migrations_to_create_table(cls):
        command = 'python manage.py makemigrations'
        CommonUtil.run_subprocess_command(command)

    @classmethod
    def insert_data_to_new_archive_table(cls, archive_table_name, data_to_insert, cursor):
        placeholders = ', '.join(['%s'] * len(data_to_insert[0]))
        columns = ', '.join(data_to_insert[0].keys())
        insert_query = "INSERT INTO {} ({}) VALUES ({})".format(archive_table_name, columns, placeholders)
        values = [tuple(row.values()) for row in data_to_insert]
        cursor.executemany(insert_query, values)

    @classmethod
    def delete_records(cls, table_name_str, records_to_delete, table_name_prefix, cursor, is_fb, app1):
        if is_fb:
            batch_ops = {}
            for unique_id in records_to_delete:
                ref = db.reference('/{}/{}'.format(table_name_str.lower(), unique_id), app=app1)
                batch_ops[unique_id] = ref.delete()
            db.reference(app=app1).update(batch_ops)
        else:
            placeholders_str = ', '.join(['%s'] * len(records_to_delete))
            query = "DELETE FROM " + table_name_prefix + "{} WHERE id IN ({})".format(table_name_str.lower(), placeholders_str)
            primary_keys = [record.id for record in records_to_delete]
            cursor.execute(query, primary_keys)

    @classmethod
    def get_data_to_insert(cls, records_to_delete, all_fields):
        all_data = []
        for record in records_to_delete:
            data = {}
            for field in all_fields:
                field_value = getattr(record, field)
                data[field] = field_value
            all_data.append(data)
        return all_data
