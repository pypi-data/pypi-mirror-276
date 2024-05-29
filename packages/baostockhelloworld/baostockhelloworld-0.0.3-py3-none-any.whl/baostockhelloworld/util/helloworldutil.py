# -*- coding:utf-8 -*-
"""
字符串方法
@author: baostock.com
@group : baostock.com
@contact: baostock@163.com
"""
import os
import sys


def sayhelloworld():
    '''
    在控制台输出HelloWorld!字符串
    '''

    msg = 'HelloWorld!'
    print(msg)

    process_date = datetime.now().strftime("%Y%m%d")
    msg2 = process_date+' baostock HelloWorld!'
    print(msg2)