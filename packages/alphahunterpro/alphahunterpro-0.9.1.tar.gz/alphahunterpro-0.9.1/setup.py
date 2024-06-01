# -*- coding:utf-8 -*-

#from distutils.core import setup
from setuptools import setup

setup(
    name="alphahunterpro",
    version="0.9.1",
    packages=[
        "quant",
        "quant.utils",
        "quant.platform",
    ],
    description="Asynchronous driven quantitative trading framework.",
    url="https://github.com/yanjlee/alphahunter",
    author="yanjlee",
    author_email="8342537@qq.com",
    license="MIT",
    keywords=[
        "alphahunter", "quant", "framework", "async", "asynchronous", "digiccy", "digital", "currency",
        "marketmaker", "binance", "okex", "huobi", "bitmex", "ftx"
    ],

    install_requires=[
        'requests',
        'faker',
        'execjs',
        'loguru',
        'base64',
        'hashlib',
        'Crypto',
        'pandas',
        'fuzzywuzzy',
        'httpx',
        'Pillow',
        'playwright',
        'PyExecJS',
        'redis',
        'fastapi',
        'uvicorn',
        'APScheduler',
        'beautifulsoup4',
        'bs4',
        'certifi',
        'clickhouse-driver',
        'curl-cffi',
        'DrissionPage',
        'fake-useragent',
        'Flask',
        'Flask-APScheduler',
        'Flask-Cors',
        'frida',
        'gevent',
        'httpx',
        'Jinja2',
        'langchain',
        'langchain-community',
        'suiutils-py',
        '58',
        "aiohttp==3.2.1",
        "aioamqp==0.13.0",
        "motor==2.0.0"
    ],
)
