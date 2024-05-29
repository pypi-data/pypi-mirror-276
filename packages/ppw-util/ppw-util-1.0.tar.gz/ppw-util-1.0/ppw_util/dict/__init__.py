# -*- coding: utf-8 -*
# #!/usr/bin/python3

# How to use: from ppw_util.dict import Dict
import time

class Dict:

    def __init__(self):
        pass

    @staticmethod
    def get_timestamp(data_struct: dict, data_field: str, date_format: str): # "%Y-%m-%d %H:%M:%S"
        if data_struct is None:
            return None
        if data_field not in data_struct:
            return None
        datetime = data_struct[data_field] if data_struct[data_field] is not None else None

        if datetime is None:
            return None
        timestamp = None
        if date_format is None:
            return datetime
        else:
            date_str = time.strptime(str(datetime), date_format)
            timestamp = time.mktime(date_str) * 1000
        return timestamp

    @staticmethod
    def get_val(data_struct: dict, data_field: str):
        if data_struct is None:
            return None
        if data_field not in data_struct:
            return None
        return data_struct[data_field] if data_struct[data_field] is not None else None

    @staticmethod
    def get_val_list(data_struct_list: list, data_field: str):
        data_val_list = []
        if data_struct_list is None:
            return data_val_list
        for data_stuct in data_struct_list:
            data_val_list.append(Dict.get_val(data_stuct, data_field))
        return data_val_list




