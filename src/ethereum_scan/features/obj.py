# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
----------------------------------------
@所属项目 : ethereum_scan
----------------------------------------
@作者     : French<1109527533@hoime.cn>
@软件     : PyCharm
@文件名   : obj.py
@创建时间 : 2022-5-23 - 17:49
@修改时间 : 2022-5-23 - 17:49
@文件说明 : 总控对象
"""
import requests
import json
from src.ethereum_scan.tool import Tool


class Key(object):
    """
    开发人员: French \n
    @创建时间: 2022-05-23 \n
    @修改时间: 2022-05-23 \n
    @功能描述: Key对象 \n
    """

    def __init__(self, api_key, api_url=None):
        if api_url is not None:
            self.api_url = api_url
        else:
            self.api_url = "https://api.etherscan.io/api"
        self.api_key = api_key


class Accounts(Key):
    # 初始化
    def __init__(self, key_conf):
        Key.__init__(self, key_conf)
        super().__init__(key_conf)
        # 重新赋值
        self.api_key = key_conf.api_key

    # 获取单个地址的ETH的余额
    def get_ether_balance_for_a_single_address(self, address, tag="latest"):
        """
        开发人员: French \n
        @创建时间: 2022-05-23 \n
        @修改时间: 2022-05-23 \n
        @功能描述: 获取单个地址中的ETH余额 \n

        Args:
            address(str): ETH/ERC20地址
            tag(str): 标签

        Returns:
            float
        """
        requests_url = self.api_url + "?"
        parameter = {
            "module": "account",
            "action": "balance",
            "address": address,
            "tag": tag,
            "apikey": self.api_key
        }
        requests_url += Tool.dict_to_url_parameter(parameter)
        try:
            # 发送请求
            response = requests.get(requests_url)
            response = json.loads(response.text)
            # 判断是否发生了错误
            if response["status"] == "1":
                # 除了余额
                eht_balance = Tool.wei_to_ether(response["result"])
                return eht_balance
            else:
                raise ValueError(response["result"])
        except requests.exceptions.ConnectionError:
            print("请求失败")

    # 获取多个地址中的ETH余额
    def get_the_ether_balance_of_multiple_addresses(self, address_list, tag="latest"):
        """
        开发人员: French \n
        @创建时间: 2022-06-02 \n
        @修改时间: 2022-06-02 \n
        @功能描述: 获取多个地址中的ETH余额 \n

        Args:
            address_list(list): ETH/ERC20地址列表
            tag(str): 标签

        Returns:
            list
        """
        requests_url = self.api_url + "?"
        # 判断参数长度
        if len(address_list) > 20:
            address_list = address_list[:20]

        parameter = {
            "module": "account",
            "action": "balancemulti",
            "address": Tool.list_to_str(address_list),
            "tag": tag,
            "apikey": self.api_key
        }

        requests_url += Tool.dict_to_url_parameter(parameter)
        try:
            # 发送请求
            response = requests.get(requests_url)
            response = json.loads(response.text)
            # 判断是否发生了错误
            if response["status"] == "1":
                # 遍历结果集
                for i in response["result"]:
                    i["balance"] = Tool.wei_to_ether(i["balance"])
                return response["result"]
            else:
                raise ValueError(response["result"])
        except requests.exceptions.ConnectionError:
            print("请求失败")

    # 按地址获取“正常”交易列表
    def get_a_list_of_normal_transactions_by_address(self, address, start_block=0, end_block=99999999, page=1,
                                                     offset=100, sort="desc"):
        """
        开发人员: French \n
        @创建时间: 2022-06-03 \n
        @修改时间: 2022-06-07 \n
        @功能描述: 按地址获取“正常”交易列表 \n

        Args:
            address(str): ETH/ERC20地址
            start_block(int): 起始块
            end_block(int): 结束块
            page(int): 页数
            offset(int): 数量
            sort(str): 排序方式

        Returns:
            list
        """
        requests_url = self.api_url + "?"
        parameter = {
            "module": "account",
            "action": "txlist",
            "address": address,
            "startblock": start_block,
            "endblock": end_block,
            "page": page,
            "offset": offset,
            "sort": sort,
            "apikey": self.api_key
        }
        requests_url += Tool.dict_to_url_parameter(parameter)
        try:
            # 发送请求
            response = requests.get(requests_url)
            response = json.loads(response.text)
            # 判断是否发生了错误
            if response["status"] == "1":
                return response["result"]
            else:
                raise ValueError(response["result"])
        except requests.exceptions.ConnectionError:
            print("请求失败")

    # 按地址获取“内部”交易列表
    def get_a_list_of_internal_transactions_by_address(self, address, start_block=0, end_block=99999999, page=1,
                                                       offset=100, sort="desc"):
        """
        开发人员: French \n
        @创建时间: 2022-06-03 \n
        @修改时间: 2022-06-08 \n
        @功能描述: 按地址获取“内部”交易列表 \n

        Args:
            address(str): ETH/ERC20地址
            start_block(int): 起始块
            end_block(int): 结束块
            page(int): 页数
            offset(int): 数量
            sort(str): 排序方式

        Returns:
            list
        """
        requests_url = self.api_url + "?"
        parameter = {
            "module": "account",
            "action": "txlistinternal",
            "address": address,
            "startblock": start_block,
            "endblock": end_block,
            "page": page,
            "offset": offset,
            "sort": sort,
            "apikey": self.api_key
        }
        requests_url += Tool.dict_to_url_parameter(parameter)
        try:
            # 发送请求
            response = requests.get(requests_url)
            response = json.loads(response.text)
            # 判断是否发生了错误
            if response["status"] == "1":
                return response["result"]
            else:
                raise ValueError(response["result"])
        except requests.exceptions.ConnectionError:
            print("请求失败")

    # 通过事务哈希获取“内部事务”
    def get_internal_transactions_by_transaction_hash(self, txhash):
        """
        开发人员: French \n
        @创建时间: 2022-06-03 \n
        @修改时间: 2022-06-08 \n
        @功能描述: 通过事务哈希获取“内部事务” \n

        Args:
            txhash(str): ETH/ERC20地址

        Returns:
            list
        """
        requests_url = self.api_url + "?"
        parameter = {
            "module": "account",
            "action": "txlistinternal",
            "txhash": txhash,
            "apikey": self.api_key
        }
        requests_url += Tool.dict_to_url_parameter(parameter)
        try:
            # 发送请求
            response = requests.get(requests_url)
            response = json.loads(response.text)
            # 判断是否发生了错误
            if response["status"] == "1":
                return response["result"]
            else:
                raise ValueError(response["result"])
        except requests.exceptions.ConnectionError:
            print("请求失败")

    # 按区块范围获取“内部交易”
    def get_internal_transactions_by_block_range(self, start_block=0, end_block=99999999, page=1, offset=100,
                                                 sort="desc"):
        """
        开发人员: French \n
        @创建时间: 2022-06-03 \n
        @修改时间: 2022-06-08 \n
        @功能描述: 按区块范围获取“内部交易” \n

        Args:
            start_block(int): 起始块
            end_block(int): 结束块
            page(int): 页数
            offset(int): 数量
            sort(str): 排序方式

        Returns:
            list
        """
        requests_url = self.api_url + "?"
        parameter = {
            "module": "account",
            "action": "txlistinternal",
            "startblock": start_block,
            "endblock": end_block,
            "page": page,
            "offset": offset,
            "sort": sort,
            "apikey": self.api_key
        }
        requests_url += Tool.dict_to_url_parameter(parameter)
        try:
            # 发送请求
            response = requests.get(requests_url)
            response = json.loads(response.text)
            # 判断是否发生了错误
            if response["status"] == "1":
                return response["result"]
            else:
                print("错误信息:")
                print(response)
                raise ValueError(response["result"])
        except requests.exceptions.ConnectionError:
            print("请求失败")

    # 按地址获取“ERC20-代币转移事件”列表
    def get_a_list_of_erc20_token_transfer_events_by_address(self, address, contract_address, start_block=0,
                                                             end_block=99999999, page=1, offset=100, sort="desc"):
        """
        开发人员: French \n
        @创建时间: 2022-06-03 \n
        @修改时间: 2022-06-08 \n
        @功能描述: 按地址获取“ERC20-代币转移事件”列表 \n

        Args:
            address(str): ETH/ERC20地址
            contract_address(str): 合约地址
            start_block(int): 起始块
            end_block(int): 结束块
            page(int): 页数
            offset(int): 数量
            sort(str): 排序方式

        Returns:
            list
        """
        requests_url = self.api_url + "?"
        parameter = {
            "module": "account",
            "action": "tokentx",
            "contractaddress": contract_address,
            "address": address,
            "startblock": start_block,
            "endblock": end_block,
            "page": page,
            "offset": offset,
            "sort": sort,
            "apikey": self.api_key
        }
        requests_url += Tool.dict_to_url_parameter(parameter)
        try:
            # 发送请求
            response = requests.get(requests_url)
            response = json.loads(response.text)
            # 判断是否发生了错误
            if response["status"] == "1":
                return response["result"]
            else:
                print("错误信息:")
                print(response)
                raise ValueError(response["result"])
        except requests.exceptions.ConnectionError:
            print("请求失败")

    # 按地址获取“ERC721 - 代币转移事件”列表
    def get_a_list_of_erc721_token_transfer_events_by_address(self, address, contract_address, start_block=0,
                                                              end_block=99999999, page=1, offset=100, sort="desc"):
        """
        开发人员: French \n
        @创建时间: 2022-06-20 \n
        @修改时间: 2022-06-20 \n
        @功能描述: 按地址获取“ERC721 - 代币转移事件”列表 \n

        Args:
            address(str): ETH/ERC20地址
            contract_address(str): 合约地址
            start_block(int): 起始块
            end_block(int): 结束块
            page(int): 页数
            offset(int): 数量
            sort(str): 排序方式

        Returns:
            list
        """
        requests_url = self.api_url + "?"
        parameter = {
            "module": "account",
            "action": "tokentx",
            "contractaddress": contract_address,
            "address": address,
            "startblock": start_block,
            "endblock": end_block,
            "page": page,
            "offset": offset,
            "sort": sort,
            "apikey": self.api_key
        }
        requests_url += Tool.dict_to_url_parameter(parameter)
        try:
            # 发送请求
            response = requests.get(requests_url)
            response = json.loads(response.text)
            # 判断是否发生了错误
            if response["status"] == "1":
                return response["result"]
            else:
                print("错误信息:")
                print(response)
                raise ValueError(response["result"])
        except requests.exceptions.ConnectionError:
            print("请求失败")

    # 按地址获取“ERC1155 - 代币转移事件”列表
    def get_a_list_of_erc1155_token_transfer_events_by_address(self, address, contract_address, start_block=0,
                                                               end_block=99999999, page=1, offset=100, sort="desc"):
        """
        开发人员: French \n
        @创建时间: 2022-06-20 \n
        @修改时间: 2022-06-20 \n
        @功能描述: 按地址获取“ERC1155 - 代币转移事件”列表 \n

        Args:
            address(str): ETH/ERC20地址
            contract_address(str): 合约地址
            start_block(int): 起始块
            end_block(int): 结束块
            page(int): 页数
            offset(int): 数量
            sort(str): 排序方式

        Returns:
            list
        """
        requests_url = self.api_url + "?"
        parameter = {
            "module": "account",
            "action": "token1155tx",
            "contractaddress": contract_address,
            "address": address,
            "startblock": start_block,
            "endblock": end_block,
            "page": page,
            "offset": offset,
            "sort": sort,
            "apikey": self.api_key
        }
        requests_url += Tool.dict_to_url_parameter(parameter)
        try:
            # 发送请求
            response = requests.get(requests_url)
            response = json.loads(response.text)
            # 判断是否发生了错误
            if response["status"] == "1":
                return response["result"]
            else:
                print("错误信息:")
                print(response)
                raise ValueError(response["result"])
        except requests.exceptions.ConnectionError:
            print("请求失败")

    # 获取按地址挖掘的区块列表
    def get_list_of_blocks_mined_by_address(self, address, block_type="blocks", page=1, offset=100):
        """
        开发人员: French \n
        @创建时间: 2022-06-20 \n
        @修改时间: 2022-06-20 \n
        @功能描述: 获取按地址挖掘的区块列表 \n

        Args:
            address(str): ETH/ERC20地址
            block_type(str): 合约地址
            page(int): 页数
            offset(int): 数量

        Returns:
            list
        """
        requests_url = self.api_url + "?"
        parameter = {
            "module": "account",
            "action": "getminedblocks",
            "address": address,
            "blocktype": block_type,
            "page": page,
            "offset": offset,
            "apikey": self.api_key
        }
        requests_url += Tool.dict_to_url_parameter(parameter)
        try:
            # 发送请求
            response = requests.get(requests_url)
            response = json.loads(response.text)
            # 判断是否发生了错误
            if response["status"] == "1":
                return response["result"]
            else:
                print("错误信息:")
                print(response)
                raise ValueError(response["result"])
        except requests.exceptions.ConnectionError:
            print("请求失败")

    # 通过 BlockNo 获取单个地址的历史以太币余额
    def get_historical_ether_balance_for_a_single_address_by_block_no(self, address, blockno):
        """
        开发人员: French \n
        @创建时间: 2022-06-20 \n
        @修改时间: 2022-06-20 \n
        @功能描述: 获取按地址挖掘的区块列表 \n

        Args:
            address(str): ETH/ERC20地址
            blockno(int): 页数

        Returns:
            list
        """
        requests_url = self.api_url + "?"
        parameter = {
            "module": "account",
            "action": "balancehistory",
            "address": address,
            "blockno": blockno,
            "apikey": self.api_key
        }
        requests_url += Tool.dict_to_url_parameter(parameter)
        try:
            # 发送请求
            response = requests.get(requests_url)
            response = json.loads(response.text)
            # 判断是否发生了错误
            if response["status"] == "1":
                return response["result"]
            else:
                print("错误信息:")
                print(response)
                raise ValueError(response["result"])
        except requests.exceptions.ConnectionError:
            print("请求失败")
