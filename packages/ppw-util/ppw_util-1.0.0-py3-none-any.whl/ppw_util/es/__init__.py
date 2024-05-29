# -*- coding: utf-8 -*
# #!/usr/bin/python3

# How to use: from ppw_util.es import ES
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json

class ES:

    _conn: Elasticsearch

    def __init__(self, host: str, port: int, username: str, password: str, need_auth: bool, max_retries: int):
        auth_str = None
        if need_auth is True:
            auth_str = username + ":" + password + "@" + host + ":" + str(port)
        else:
            auth_str = host + ":" + str(port)
        self._conn = Elasticsearch([auth_str], max_retries=3)

    def get_count(self, index: str, body: dict):
        data = self._conn.count(
            index = index,
            body = body
        )
        return data

    def is_exist(self, index:str, id: str):
        return self._conn.exists(index = index, id = id)

    def fetch_one(self, index: str, doc_type: str, id: str):
        return self._conn.get(index = index, doc_type = doc_type, id = id)

    def del_one(self, index: str, doc_type: str, id: str):
        is_success = False
        try:
            self._conn.delete(index = index, doc_type = doc_type, id = id)
            is_success = True
        except:
            is_success = False
        return is_success
    
    def update_one(self, index:str, doc_type: str, id: str, body: dict):
        is_success = False
        try:
            self._conn.update(index = index, doc_type = doc_type, body = body, id = id)
            is_success = True
        except:
            is_success = False
        return is_success
    
    def get_scroll(self, index: str, _source, body, size, process_target):
        body["_source"] = _source
        result = self._conn.search(
            index = index,
            scroll = "5m",
            timeout = "1m",
            size = size,
            body = body
        )
        hits = result["hits"]["hits"]
        total = result["hits"]["total"]["value"]
        for item in hits:
            self.parse_hit(item, _source, process_target)
        
        scroll_id = result["_scroll_id"]
        for i in range(int(total / size)):
            res = self._conn.scroll(scroll_id = scroll_id, scroll='5m')
            hits = res["hits"]["hits"]
            for item in hits:
                self.parse_hit(item, _source, process_target)
        self._conn.clear_scroll(scroll_id = scroll_id)

    def parse_hit(self, item, _source, process_target):
        source = item["_source"]
        vals = []
        for key in _source:
            if "." in key:
                sub_vals = []
                sub_keys = key.split(".")
                sub_source_key = sub_keys[0]
                sub_key = sub_keys[1]
                if sub_source_key in source:
                    sub_source = source[sub_source_key]
                    if isinstance(sub_source, list):
                        # 数组处理
                        for sub_item in sub_source:
                            sub_val = sub_item[sub_key]
                            sub_vals.append(sub_val)
                        value = sub_vals
                    else:
                        # 字典处理
                        sub_val = sub_source[sub_key]
                        value = sub_val
            elif key == "_id":
                value = item["_id"]
            elif key == "_index":
                value = item["_index"]
            else:
                if key in source:
                    value = source[key]
                else:
                    value = None
            vals.append(value)
        process_target(vals)



