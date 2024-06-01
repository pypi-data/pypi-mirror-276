#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Name    : setup.py
# @Author  : yanlee

import setuptools
import shutil

# 删除dist/目录
shutil.rmtree('dist', ignore_errors=True)

setuptools.setup(
    name="Titan-pro",
    version="1.2.1",
    author="yanjlee",
    author_email="yanjlee@163.com",
    description="Titan is a totally free cryptocurrency automated trading framework for traders of all skill levels. Built on top of the ccxt API library, it works out of the box with any exchange and trading pair. We believe in decentralizing trading strategies and providing everyone access to building advanced crypto portfolios. The future of algorithmic trading is here!.",  # 模块简介
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
    ],
    long_description=open(r'readme.md', encoding='utf-8').read(),  # 读取readme自述文件
    long_description_content_type="text/markdown",
    url="https://github.com/yanjlee/Titan",  # 模块github地址
    packages=setuptools.find_packages(),     # 自动列出项目下的包
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",   # 开源许可证
        "Operating System :: OS Independent",      # 这里的定义是系统无关（全平台兼容），如果你的包只能在部分特定系统上运行，需要修改。
    ],
)