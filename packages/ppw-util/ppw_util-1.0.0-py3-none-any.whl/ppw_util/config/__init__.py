# -*- coding: utf-8 -*
# #!/usr/bin/python3

# How to use: from ppw_util.config import Config
import configparser
from ppw_util.rsa import HandleRSA

class Config:
    # 配置文件
    APP_CONFIG = "/app.conf"
    DB_CONFIG = "/db.conf"
    RPC_CONFIG = "/rpc.conf"

    # 不同环境路径
    PROD_PATH = "/prod"
    DEV_PATH = "/dev"

    _is_prod: bool
    _app_conf: configparser.ConfigParser
    _db_conf: configparser.ConfigParser
    _rpc_conf: configparser.ConfigParser

    def __init__(self, base_path: str, encoding: str):
        self._app_conf = configparser.ConfigParser()
        self._app_conf.read(base_path + self.APP_CONFIG, encoding=encoding)
        self._is_prod = self._app_conf.getboolean("main", "is_prod")
        self._db_conf = configparser.ConfigParser()
        self._rpc_conf = configparser.ConfigParser()
        if self._is_prod:
            self._db_conf.read(base_path + self.PROD_PATH + self.DB_CONFIG, encoding=encoding)
            self._rpc_conf.read(base_path + self.PROD_PATH + self.RPC_CONFIG, encoding=encoding)
        else:
            self._db_conf.read(base_path + self.DEV_PATH + self.DB_CONFIG, encoding=encoding)
            self._rpc_conf.read(base_path + self.DEV_PATH + self.RPC_CONFIG, encoding=encoding)

    def get_db_config(self) -> configparser.ConfigParser:
        return self._db_conf

    def get_rpc_config(self) -> configparser.ConfigParser:
        return self._rpc_conf

    def get_secret_val(self, config: configparser.ConfigParser, section: str, key: str):
        if self._is_prod:
            return HandleRSA.decrypt(config.get(section, key))
        else:
            return config.get(section, key)
