# coding:utf-8
from setuptools import setup
setup(
        name='ppw-util',
        version='1.0',
        description='This is a ppw-util',
        author='yi.xu',
        author_email='widebluesky@qq.com',
        url='',
        packages=[
                'ppw_util.file', 
                'ppw_util.lark',
                'ppw_util.mysql',
                'ppw_util.mongo',
                'ppw_util.es',
                'ppw_util.rabbitmq',
                'ppw_util.dict',
                'ppw_util.config',
                'ppw_util.log'
        ]
)
