# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

long_desc = """
BaoStock
===============

* This is a testing project that outputs helloworld string information on the console


Target Users
--------------


Installation
--------------

    pip install baostockhelloworld

Upgrade
---------------

    pip install baostockhelloworld --upgrade

Quick Start
--------------

::

    import baostockhelloworld as bshw


    # 
    bshw.sayhelloworld()

return::

    HelloWorld!

"""


setup(
    name='baostockhelloworld',
    version='0.0.4',
    description=(
        'A tool for outputs helloworld string information on the console'
    ),
    long_description=long_desc,
    author='baostock',
    author_email='baostock@163.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='http://www.baostock.com',
    install_requires=[
        'pandas>=0.18.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',   # 开发状态
        'Environment :: Console',  # 运行环境
        'License :: OSI Approved :: BSD License',  # BSD协议
        'Operating System :: OS Independent',  # 与平台无关
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)
