from abc import abstractmethod, ABC


class DataPurgingInterface(ABC):

    @abstractmethod
    def get_count_of_records_between_interval_dates(self, interval_start_date, interval_end_date, main_table_name):
        pass

    @abstractmethod
    def get_stale_records(self, main_table_name, interval_start_date, interval_end_date, all_fields, table_name_str, db_record_size, app1):
        pass
