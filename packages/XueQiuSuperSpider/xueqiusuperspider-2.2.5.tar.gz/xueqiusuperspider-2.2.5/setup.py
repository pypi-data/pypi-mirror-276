#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Name    : setup.py
# @Author  : yanlee

import setuptools
import shutil

# 删除dist/目录
shutil.rmtree('dist', ignore_errors=True)

setuptools.setup(
    name="XueQiuSuperSpider",
    version="2.2.5",
    author="yanjlee",
    author_email="yanjlee@163.com",
    description="雪球超级爬虫的所有组件互相没有任何依赖，包括参数。整体架构由Collector、Mapper以及Consumer三个接口支撑。功能分别为数据搜集、数据相关信息（分支信息）的组装、以及最终的数据分析，三个接口定义了整个数据抓取生命周期的三个阶段。Mapper组件可以进行多次嵌套，就像流水线一样，不同的Mapper负责自己对应的组装任务，经过N个Mapper，完成一个对象的N种属性组装，当然，如果你不需要某些属性，你完全可以跳过某些mapper，这样可以节省许多抓取时间。在参数传递方面，模块在处理参数之前会对参数进行深度复制，确保不会出现多线程同步问题，模块内部参数严格定义为只读。变量只局限在方法范围内，完全避免了线程间数据共享。.",  # 模块简介
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
    url="https://github.com/yanjlee/XueQiuSuperSpider",  # 模块github地址
    packages=setuptools.find_packages(),     # 自动列出项目下的包
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",   # 开源许可证
        "Operating System :: OS Independent",      # 这里的定义是系统无关（全平台兼容），如果你的包只能在部分特定系统上运行，需要修改。
    ],
)