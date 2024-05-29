# -*- coding: utf-8 -*
# #!/usr/bin/python3

# How to use: from ppw_util.mysql import Mysql
import pymysql

class Mysql:

    _conn: pymysql.connections.Connection

    def __init__(self, host: str, port: int, database: str, username: str, password: str):
        self._conn = pymysql.connect(host=host, port=port, db=database, user=username, password=password)

    def execute(self, sql: str):
        if sql is None:
            return None
        self._conn.ping(reconnect=True)
        cursor = self._conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        self._conn.commit()
        return None

    def get_count(self, sql: str, count_key: str):
        if sql is None:
            return 0
        self._conn.ping(reconnect=True)
        cursor = self._conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        return cursor.fetchone()[count_key]

    def fetch_one(self, sql: str):
        if sql is None:
            return None
        self._conn.ping(reconnect=True)
        cursor = self._conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        data = cursor.fetchone()
        return data

    def fetch_list(self, sql: str):
        if sql is None:
            return []
        self._conn.ping(reconnect=True)
        cursor = self._conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        data = cursor.fetchall()
        return data

    def fetch_data(self, table: str, sharding_num: str, conds: dict, is_multiple: bool, offset: int = 0, limit: int = 10):
        sql_arr = []
        if sharding_num is None:
            sql_arr = ["SELECT * FROM", table]
        else:
            sql_arr = ["SELECT * FROM", table + "_" + sharding_num]
        if len(conds) > 0:
            sql_arr.append("WHERE")
            conds_arr = []
            for key, value in conds.items():
                conds_arr.append(key + "=" + "'" + str(value) + "'")
            conds_str = ' AND '.join(conds_arr)
            sql_arr.append(conds_str)
        if is_multiple:
            sql_arr.append("LIMIT " + str(offset) + "," + str(limit))
            sql = ' '.join(sql_arr)
            data = self.fetch_list(sql)
        else: 
            sql = ' '.join(sql_arr)
            data = self.fetch_one(sql)
        return data