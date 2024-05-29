# -*- coding: utf-8 -*
# #!/usr/bin/python3

# How to use: from ppw_util.lark import Lark
import requests
import json

class Lark:

    CONTENT_TYPE: str = "application/json"

    def __init__(self):
        pass

    @classmethod
    def send(self, api: str, params: dict = {}, content_type: str = CONTENT_TYPE):
        headers = {
            "Content-Type": content_type,
        }
        r = requests.post(api, headers=headers, params=params)
        if r is not None and r.status_code == 200:
            json_obj = json.loads(r.text)
            return json_obj
        return None