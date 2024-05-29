# -*- coding: utf-8 -*
# #!/usr/bin/python3

# How to use: from ppw_util.mongo import Mongo
import pymongo

class Mongo:

    _conn: pymongo.MongoClient

    def __init__(self, host: str, port: int, database: str, username: str, password: str, need_auth: bool, auth_source: str):
        auth_str = None
        if need_auth is True:
            auth_str = "mongodb://" + username + ":" + password + "@" + host + ":" + str(port) + "/"
            if auth_source is not None:
                auth_str = auth_str + "?authSource=" + auth_source
        else:
            auth_str = "mongodb://" + host + ":" + str(port) + "/"

        self._conn = pymongo.MongoClient(auth_str)
        self._db = self._conn[database]

    def get_count(self, table: str, conds: dict):
        table_obj = self._db[table]
        return table_obj.count_documents(conds)

    def fetch_one(self, table: str, conds: dict):
        table_obj = self._db[table]
        data = table_obj.find_one(conds)
        return data

    def fetch_list(self, table : str, conds: dict):
        table_obj = self._db[table]
        return table_obj.find(conds)

    def del_one(self, table, conds: dict):
        is_success = False
        try:
            table_obj = self._db[table]
            result = table_obj.delete_one(conds)
            is_success = True
        except Exception as e:
            raise e
            # is_success = False
        return is_success
    
    def del_list(self, table, conds: dict):
        is_success = False
        try:
            table_obj = self._db[table]
            result = table_obj.delete_many(conds)
            is_success = True
        except Exception as e:
            raise e
            # is_success = False
        return is_success
