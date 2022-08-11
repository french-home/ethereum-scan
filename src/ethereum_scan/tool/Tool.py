# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
----------------------------------------
@所属项目 : ethereum_scan
----------------------------------------
@作者     : French<1109527533@hoime.cn>
@软件     : PyCharm
@文件名   : Tool.py
@创建时间 : 2022-5-23 - 17:26
@修改时间 : 2022-5-23 - 17:26
@文件说明 : 工具组
"""


def wei_to_ether(numerical_value):
    """
    开发人员: French \n
    @创建时间: 2022-05-23 \n
    @修改时间: 2022-05-23 \n
    @功能描述: wei转换为ether \n

    Args:
        numerical_value(int): 数值

    Returns:
        float
    """
    numerical_value = int(numerical_value) / 1000000000000000000
    numerical_value = round(numerical_value, 6)
    return numerical_value


def dict_to_url_parameter(data_dict, joiner="&"):
    """
    开发人员: French \n
    @创建时间: 2022-06-01 \n
    @修改时间: 2022-06-01 \n
    @功能描述: 字典转换为url参数 \n

    Args:
        data_dict(dict): 数据列表
        joiner(str): 连接符

    Returns:
        str
    """
    dict_length = len(data_dict.keys())
    url_parameter = ""
    counter = 0
    for i in data_dict.keys():
        counter += 1
        url_parameter += i + "=" + str(data_dict[i])
        if counter < dict_length:
            url_parameter += joiner
    return url_parameter


def list_to_str(data_list, joiner=","):
    """
    开发人员: French \n
    @创建时间: 2022-06-01 \n
    @修改时间: 2022-06-01 \n
    @功能描述: wei转换为ether \n

    Args:
        data_list(list): 数据列表
        joiner(str): 连接符

    Returns:
        str
    """
    data_length = len(data_list)
    url_parameter = ""
    counter = 0
    for i in data_list:
        counter += 1
        url_parameter += i
        if counter < data_length:
            url_parameter += joiner
    return url_parameter


if __name__ == '__main__':
    test = ["a", "b", "c", "d"]
    print(list_to_str(test))
    pass