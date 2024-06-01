# coding: utf-8
# Project：erp_sdk_python
# File：itemtool.py
# Author：李福成
# Date ：2024/5/7 上午10:42
# IDE：PyCharm
from typing import Optional

from erp_apis.erpRequest import Request
from erp_apis.utils.util import getDefaultParams, JTable1, dumps


def ItemApiRequest(
        json: dict,
        url: str = '/erp/webapi/ItemApi/CombineSku/GetEditOrCreateCombineSku', **kwargs
) -> Request:
    return Request(
        method='POST',
        url=url,
        json=json,
        callback=JTable1,
        hostType='erpApi'
    )


def GetEditOrCreateCombineSku(data = str):
    '''
    获取组合商品资料
    :param page_num: 页数
    :param page_size:  每页条数
    :param queryData:  查询条件
    :return: 查询结果
    '''
    return ItemApiRequest(
        json={
            "ip": "",
            "uid": "15424700",
            "coid": "10174711",
            "data": data
        },
        method='LoadDataToJSON',
        params={'archive': 'false'}
    )

# itemContrast
