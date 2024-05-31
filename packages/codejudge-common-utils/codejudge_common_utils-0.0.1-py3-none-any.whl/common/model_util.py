from django.db import models


class ModelUtil:

    @classmethod
    def get_all_field_names(cls, model, ignore_fields=[], prepend_table_name=False, table_name=''):
        prefix = table_name + '.' if prepend_table_name is True else ''
        field_names = []
        for f in model._meta.get_fields():
            field_name = f.name
            if field_name not in ignore_fields:
                field_names.append(prefix + f.name)
        return field_names

    @classmethod
    def get_all_fields_name_of_current_table(cls, model, ignore_fields=[], prepend_table_name=False, table_name=''):
        prefix = table_name + '.' if prepend_table_name is True else ''
        field_names = []
        for field in model._meta.get_fields():
            if isinstance(field, models.ManyToOneRel):
                continue
            if field.is_relation and field.many_to_one or not field.auto_created:
                field_name = field.get_attname()
            else:
                field_name = field.name

            if field_name not in ignore_fields:
                field_names.append(prefix + field_name)
        return field_names