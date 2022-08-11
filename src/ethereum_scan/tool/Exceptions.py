# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
----------------------------------------
@所属项目 : ethereum_scan
----------------------------------------
@作者     : French<1109527533@hoime.cn>
@软件     : PyCharm
@文件名   : Exceptions.py
@创建时间 : 2022-6-2 - 11:02
@修改时间 : 2022-6-2 - 11:02
@文件说明 : 自定义异常
"""


# 通用异常
class UniversalExceptions(object):

    class RequestError(Exception):
        def __str__(self):
            print("请求错误")
