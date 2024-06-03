# common_library/list_util.py
from rest_framework import status

from common.config import get_config_module


class ListUtil:

    @classmethod
    def sort(cls, arr, field, in_increasing_order=True, raise_exception_if_field_not_present=True):
        config = get_config_module()
        DevException = config.DevException
        if arr:
            for item in arr:
                if field not in item:
                    if raise_exception_if_field_not_present:
                        raise DevException(message=field + ' not present in one or more objects in the list!',
                                           status=status.HTTP_400_BAD_REQUEST)
                    return arr

            return sorted(arr, key=lambda i: i[field], reverse=not in_increasing_order)
        return arr

    @classmethod
    def sort_by_two_fields(cls, arr, field_sort_order_tuples):
        if ListUtil.is_valid(arr):
           return sorted(arr, key=lambda i: (i[field_sort_order_tuples[0][0]] * (1 if field_sort_order_tuples[0][1] is True else -1),
                                             i[field_sort_order_tuples[1][0]] * (1 if field_sort_order_tuples[1][1] is True else -1)))
        return arr

    @classmethod
    def is_valid(cls, items):
        return items and len(items) > 0

    @classmethod
    def convert_list_to_map(cls, items):
        if ListUtil.is_valid(items):
            return dict.fromkeys(items, True)
        return None

    @classmethod
    def convert_list_to_map_by_field(cls, items, field):
        if ListUtil.is_valid(items):
            item_map = dict()
            for item in items:
                item_map[item[field]] = item
            return item_map
        return None

    @classmethod
    def convert_to_flat_list(cls, list_of_list):
        return [item for sublist in list_of_list for item in sublist]

    @classmethod
    def get_field_value_list(cls, items, field):
        field_value_list = []
        if ListUtil.is_valid(items):
            for item in items:
                field_value_list.append(item[field])
        return field_value_list
