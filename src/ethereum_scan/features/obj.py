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
from ethereum_scan.tool import Tool


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


# 账户
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
                eth_balance = Tool.wei_to_ether(response["result"])
                return eth_balance
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
            block_type(str): 区块类型
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
            blockno(int): 区块号

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
                # 除了余额
                eth_balance = Tool.wei_to_ether(response["result"])
                return eth_balance
            else:
                print("错误信息:")
                print(response)
                raise ValueError(response["result"])
        except requests.exceptions.ConnectionError:
            print("请求失败")


# 交易
class Transactions(Key):
    # 初始化
    def __init__(self, key_conf):
        Key.__init__(self, key_conf)
        super().__init__(key_conf)
        # 重新赋值
        self.api_key = key_conf.api_key

    # 检查合约执行状态
    def check_contract_execution_status(self, txhash):
        """
        开发人员: French \n
        @创建时间: 2022-12-04 \n
        @修改时间: 2022-12-04 \n
        @功能描述: 检查合约执行状态 \n

        Args:
            txhash(str): 交易的Hash值

        Returns:
            dict
        """
        requests_url = self.api_url + "?"
        parameter = {
            "module": "transaction",
            "action": "getstatus",
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
                print("错误信息:")
                print(response)
                raise ValueError(response["result"])
        except requests.exceptions.ConnectionError:
            print("请求失败")

    # 检查交易执行状态
    def check_transaction_receipt_status(self, txhash):
        """
        开发人员: French \n
        @创建时间: 2022-12-04 \n
        @修改时间: 2022-12-04 \n
        @功能描述: 检查交易执行状态 \n

        Args:
            txhash(str): 交易的Hash值

        Returns:
            dict
        """
        requests_url = self.api_url + "?"
        parameter = {
            "module": "transaction",
            "action": "gettxreceiptstatus",
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
                print("错误信息:")
                print(response)
                raise ValueError(response["result"])
        except requests.exceptions.ConnectionError:
            print("请求失败")


# 日志
class Logs(Key):
    # 初始化
    def __init__(self, key_conf):
        Key.__init__(self, key_conf)
        super().__init__(key_conf)
        # 重新赋值
        self.api_key = key_conf.api_key

    # Get Event Logs by Address
    def get_event_logs_by_address(self, address, from_block, to_block, page, offset):
        """
        @开发人员: French \n
        @创建时间: 2023-03-09 \n
        @修改时间: 2023-12-25 \n
        @功能描述: 根据ERC-20地址，获取区块时间日志 \n

        Args:
            address(str): ERC-20地址
            from_block(int): 来自块
            to_block(int): 到快
            page(int): 页数
            offset(int): 数量

        Returns:
            dict
        """
        requests_url = self.api_url + "?"
        parameter = {
            "module": "logs",
            "action": "getLogs",
            "address": address,
            "fromBlock": from_block,
            "toBlock": to_block,
            "page": page,
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

    pass


# 代币
class Tokens(Key):
    # 初始化
    def __init__(self, key_conf):
        Key.__init__(self, key_conf)
        super().__init__(key_conf)
        # 重新赋值
        self.api_key = key_conf.api_key

    # 根据ERC-20合约地址, 获取代币总量
    def get_erc20_token_total_supply_by_contract_address(self, contractaddress):
        """
        开发人员: French \n
        @创建时间: 2022-12-08 \n
        @修改时间: 2022-12-08 \n
        @功能描述: 根据ERC-20合约地址, 获取代币总量\n

        Args:
            contractaddress(str): ERC-20合约地址

        Returns:
            dict
        """
        requests_url = self.api_url + "?"
        parameter = {
            "module": "stats",
            "action": "tokensupply",
            "contractaddress": contractaddress,
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

    # 根据ERC-20合约地址, 获取目标地址持有的代币余额
    def get_erc20_token_account_balance_for_token_contract_address(self, contractaddress, address):
        """
        开发人员: French \n
        @创建时间: 2022-12-08 \n
        @修改时间: 2022-12-08 \n
        @功能描述: 根据ERC-20合约地址, 获取目标地址持有的代币余额\n

        Args:
            contractaddress(str): ERC-20合约地址
            address(str): ETH/ERC20地址

        Returns:
            dict
        """
        requests_url = self.api_url + "?"
        parameter = {
            "module": "account",
            "action": "tokenbalance",
            "contractaddress": contractaddress,
            "address": address,
            "tag": "latest",
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

    # 根据ERC-20合约地址和块号, 获取历史代币总量 -- PRO
    def get_historical_erc20_token_total_supply_by_contract_address_and_block_no(self, contractaddress, blockno):
        """
        开发人员: French \n
        @创建时间: 2022-12-08 \n
        @修改时间: 2022-12-08 \n
        @功能描述: 根据ERC-20合约地址和块好, 获取历史代币总量 --- PRO \n

        Args:
            contractaddress(str): ERC-20合约地址
            blockno(int): 块编号

        Returns:
            dict
        """
        requests_url = self.api_url + "?"
        parameter = {
            "module": "stats",
            "action": "tokensupplyhistory",
            "contractaddress": contractaddress,
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

    # 根据ERC-20合约地址和块号, 获取目标地址的历史持有的代币余额 -- PRO
    def get_historical_erc20_token_account_balance_for_token_contract_address_by_block_no(self, contractaddress,
                                                                                          address, blockno):
        """
        开发人员: French \n
        @创建时间: 2022-12-08 \n
        @修改时间: 2022-12-08 \n
        @功能描述: 据ERC-20合约地址和块号, 获取目标地址的历史持有的代币余额 --- PRO\n

        Args:
            contractaddress(str): ERC-20合约地址
            address(str): ETH/ERC20地址
            blockno(int): 块编号

        Returns:
            dict
        """
        requests_url = self.api_url + "?"
        parameter = {
            "module": "account",
            "action": "tokenbalancehistory",
            "contractaddress": contractaddress,
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

    # 根据ERC-20合约地址, 获取代币持有者列表 -- PRO
    def get_token_holder_list_by_contract_address(self, contractaddress, page=1, offset=100):
        """
        开发人员: French \n
        @创建时间: 2022-12-08 \n
        @修改时间: 2022-12-08 \n
        @功能描述: 根据ERC-20合约地址, 获取代币持有者列表 -- PRO\n

        Args:
            contractaddress(str): ERC-20合约地址
            page(int): 页数
            offset(int): 数量

        Returns:
            dict
        """
        requests_url = self.api_url + "?"
        parameter = {
            "module": "token",
            "action": "tokenholderlist",
            "contractaddress": contractaddress,
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

    # 根据ERC-20合约地址, 获取代币信息 -- PRO
    def get_token_info_by_contract_address(self, contractaddress):
        """
        开发人员: French \n
        @创建时间: 2022-12-08 \n
        @修改时间: 2022-12-08 \n
        @功能描述: 根据ERC-20合约地址, 获取代币信息 -- PRO \n

        Args:
            contractaddress(str): ERC-20合约地址

        Returns:
            dict
        """
        requests_url = self.api_url + "?"
        parameter = {
            "module": "token",
            "action": "tokeninfo",
            "contractaddress": contractaddress,
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

    # 根据ERC-20地址, 获取代币持有量 -- PRO
    def get_address_erc20_token_holding(self, address, page=1, offset=100):
        """
        开发人员: French \n
        @创建时间: 2023-03-09 \n
        @修改时间: 2023-03-09 \n
        @功能描述: 根据ERC-20地址, 获取代币持有量 -- PRO \n

        Args:
            address(str): ERC-20地址
            page(int): 页数
            offset(int): 数量

        Returns:
            dict
        """
        requests_url = self.api_url + "?"
        parameter = {
            "module": "account",
            "action": "addresstokenbalance",
            "address": address,
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

    # 根据ERC-721地址, 获取代币持有量 -- PRO
    def get_address_erc721_token_holding(self, address, page=1, offset=100):
        """
        开发人员: French \n
        @创建时间: 2023-03-09 \n
        @修改时间: 2023-03-09 \n
        @功能描述: 根据ERC-721地址, 获取代币持有量 -- PRO \n

        Args:
            address(str): ERC-721地址
            page(int): 页数
            offset(int): 数量

        Returns:
            dict
        """
        requests_url = self.api_url + "?"
        parameter = {
            "module": "account",
            "action": "addresstokennftbalance",
            "address": address,
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

    # 根据ERC-721合约地址, 获取代币库存 -- PRO
    def get_address_erc721_token_inventory_by_contract_address(self, address, contractaddress, page=1, offset=100):
        """
        开发人员: French \n
        @创建时间: 2023-03-10 \n
        @修改时间: 2023-03-10 \n
        @功能描述: 根据ERC-721合约地址, 获取代币库存  -- PRO \n

        Args:
            address(str): ERC-721地址
            contractaddress(str): 合约地址
            page(int): 页数
            offset(int): 数量

        Returns:
            dict
        """
        requests_url = self.api_url + "?"
        parameter = {
            "module": "account",
            "action": "addresstokennftinventory",
            "address": address,
            "contractaddress": contractaddress,
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


# 气体追踪器
class GasTracker(Key):
    # 初始化
    def __init__(self, key_conf):
        Key.__init__(self, key_conf)
        super().__init__(key_conf)
        # 重新赋值
        self.api_key = key_conf.api_key

    # 获取估计的确认时间
    def get_estimation_of_confirmation_time(self, gas_price):
        """
        开发人员: French \n
        @创建时间: 2023-03-15 \n
        @修改时间: 2023-03-15 \n
        @功能描述: 获取估计的确认时间\n

        Args:
            gas_price(str): Gas价格

        Returns:
            dict
        """
        requests_url = self.api_url + "?"
        parameter = {
            "module": "gastracker",
            "action": "gasestimate",
            "gasprice": gas_price,
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

    # 获取Gas预估
    def get_gas_oracle(self):
        """
        开发人员: French \n
        @创建时间: 2023-03-15 \n
        @修改时间: 2023-03-15 \n
        @功能描述: 获取Gas预估\n

        Returns:
            dict
        """
        requests_url = self.api_url + "?"
        parameter = {
            "module": "gastracker",
            "action": "gasoracle",
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

    # 获取每日平均 Gas 限制 -- PRO
    def get_daily_average_gas_limit(self, start_date, end_date, sort="asc"):
        """
        开发人员: French \n
        @创建时间: 2023-03-15 \n
        @修改时间: 2023-03-15 \n
        @功能描述: 获取估计的确认时间\n

        Args:
            start_date(str): Gas价格
            end_date(str): Gas价格
            sort(str): Gas价格

        Returns:
            dict
        """
        requests_url = self.api_url + "?"
        parameter = {
            "module": "stats",
            "action": "dailyavggaslimit",
            "startdate": start_date,
            "enddate": end_date,
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

    # 获取以太坊每日总 Gas 量 -- PRO
    def get_ethereum_daily_total_gas_used(self, start_date, end_date, sort="asc"):
        """
        开发人员: French \n
        @创建时间: 2023-03-15 \n
        @修改时间: 2023-03-15 \n
        @功能描述: 获取估计的确认时间\n

        Args:
            start_date(str): Gas价格
            end_date(str): Gas价格
            sort(str): Gas价格

        Returns:
            dict
        """
        requests_url = self.api_url + "?"
        parameter = {
            "module": "stats",
            "action": "dailygasused",
            "startdate": start_date,
            "enddate": end_date,
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

    # 获取每日平均 Gas 价格 -- PRO
    def get_daily_average_gas_price(self, start_date, end_date, sort="asc"):
        """
        开发人员: French \n
        @创建时间: 2023-03-15 \n
        @修改时间: 2023-03-15 \n
        @功能描述: 获取估计的确认时间\n

        Args:
            start_date(str): Gas价格
            end_date(str): Gas价格
            sort(str): Gas价格

        Returns:
            dict
        """
        requests_url = self.api_url + "?"
        parameter = {
            "module": "stats",
            "action": "dailyavggasprice",
            "startdate": start_date,
            "enddate": end_date,
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
