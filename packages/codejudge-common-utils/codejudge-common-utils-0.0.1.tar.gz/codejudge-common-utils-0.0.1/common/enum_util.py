class EnumUtil:

    @classmethod
    def get_enum_from_first_arg(cls, value, enum_class):
        for member in enum_class:
            status_num = member.value[0]
            if status_num == value:
                return member
        return ValueError('No enum found for value: {}'.format(value))

    @classmethod
    def get_enum_from_enum_value(cls, value, enum_class):
        for member in enum_class:
            status_num = member.value
            if status_num == value:
                return member
        return ValueError('No enum found for value: {}'.format(value))

    @classmethod
    def get_second_arg_from_first_arg(cls, value, enum_class):
        for member in enum_class:
            status_num = member.value[0]
            if status_num == value:
                return member.value[1]
        return ValueError('No enum found for value: {}'.format(value))

    @classmethod
    def get_fourth_arg_from_first_arg(cls, value, enum_class):
        for member in enum_class:
            status_num = member.value[0]
            if status_num == value:
                return member.value[3]
        return ValueError('No enum found for value: {}'.format(value))

    @classmethod
    def get_first_arg_from_third_arg(cls, value, enum_class):
        for member in enum_class:
            status_num = member.value[2]
            if status_num == value:
                return member.value[0]
        return ValueError('No enum found for value: {}'.format(value))

    @classmethod
    def get_enum_value_from_enum_name(cls, inp_enum_name, enum_class):
        for member in enum_class:
            enum_name = member.name
            if enum_name == inp_enum_name:
                return member.value
        return ValueError('No enum found for enum name: {}'.format(inp_enum_name))

    @classmethod
    def get_enum_value_from_enum_name_tuple(cls, inp_enum_name, enum_class, tuple_index):
        for member in enum_class:
            enum_name = member.name
            if enum_name == inp_enum_name:
                return member.value[tuple_index]
        return ValueError('No enum found for enum name: {}'.format(inp_enum_name))
