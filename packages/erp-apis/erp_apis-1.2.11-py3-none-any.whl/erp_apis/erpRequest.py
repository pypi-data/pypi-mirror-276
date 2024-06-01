# coding: utf-8
# Project：invoices
# File：request.py
# Author：李福成
# Date ：2024-04-09 11:20
# IDE：PyCharm
import os
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urljoin

import requests
from lxml import etree
from requests import Session as S, Request as Req, Response as Res
import time, json as j
from erp_apis.config import DEFAULT_HEADERS, Erp321BaseUrl, ErpApiBaseUrl, ErpGoodsBaseUrl


@dataclass
class UserInfoType:
    u_cid: Optional[str]
    u_co_id: Optional[str]
    u_co_name: Optional[str]
    u_id: Optional[str]
    u_name: Optional[str]
    u_lid: Optional[str]

    def __init__(self, **kwargs): pass


class Session(S):
    def __init__(self):
        super().__init__()
        self.headers.update(DEFAULT_HEADERS)
        self.proxies = {'http': "", 'https': ""}
        self.viewstateItems = dict()
        self.userInfo: Optional[UserInfoType]
        self.authorization = None

    def erpSend(self, request: Req, **kwargs) -> Res:
        if not request.headers: request.headers.update(self.headers)
        hostType = getattr(request, 'hostType', None)
        if hostType:
            resp = getattr(self, hostType + "Send", None)(request, **kwargs)
            if resp is None:
                raise Exception(f"{hostType}没有这个域的send方法")
            return resp
        raise Exception('hostType is None')

    def erp321Send(self, request, **kwargs):
        request.url = urljoin(Erp321BaseUrl, request.url)
        if request.method == 'POST':
            request.headers.update({'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
            request.data.update({k: v for k, v in self.get_viewstate(request.url).items() if k and k != "updateTime"})

        res = super().send(self.prepare_request(request), **kwargs)

        if request.callback:
            return request.callback(res)
        return res

    def erpApiSend(self, request, **kwargs):
        request.url = urljoin(ErpApiBaseUrl, request.url)
        res = super().send(self.prepare_request(request), **kwargs)
        if request.callback:
            if request.callback == 'login':
                if res.json().get('code') == 0:
                    self.userInfo = UserInfoType(**res.json().get('cookie'))
                    # self.authorization = self.epaasJointLoginGyl().get('data').get('access_token')
                else:
                    raise Exception(res.json().get('msg'))
            else:
                return request.callback(res)
        return res

    def erpGoodsSend(self, request, **kwargs):
        request.headers.update({
             'accept': 'application/json',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://goods.scm121.com',
            'priority': 'u=1, i',
            'referer': 'https://goods.scm121.com/manage/goods/goodsManage/index?eTicket=JQing6&f=erp&m=n&y=20220701&_c=jst-epaas&epaas=true&serviceKey=shop_goods',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'source': 'SUPPLIER',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',

        })
        request.url = urljoin(ErpGoodsBaseUrl, request.url)
        if self.authorization:
            request.headers['Authorization'] = self.authorization


        res = super().send(self.prepare_request(request), **kwargs)
        return res

    def get_viewstate(self, url):
        if self.viewstateItems.get(url) and self.viewstateItems.get(url).get("updateTime") > time.time() - 60 * 5:
            return self.viewstateItems.get(url)
        if not self.viewstateItems.get(url):
            self.viewstateItems.update({url: {"updateTime": time.time()}})
        res = self.get(url)
        etree_xpath = etree.HTML(res.text)

        def extract_first(xpath):
            r = etree_xpath.xpath(xpath)
            return r[0] if r else None

        self.viewstateItems.get(url).update(
            {
                "__VIEWSTATE": extract_first("//*[@id='__VIEWSTATE']/@value"),
                "__VIEWSTATEGENERATOR": extract_first("//*[@id='__VIEWSTATEGENERATOR']/@value"),
                "__EVENTVALIDATION": extract_first("//*[@id='__EVENTVALIDATION']/@value"),
            }
        )
        return self.viewstateItems.get(url)

    # 获取Authorization
    def epaasJointLoginGyl(self):
        res = self.erpSend(Request(
            method='post',
            hostType='erpGoods',
            url="/api/auth/open/epaasJointLoginGyl",
            json={
                "eTicket": "JQing6",
                "serviceKey": "shop_goods"
            }
        ))
        res = self.erpSend(Request(
            method='post',
            hostType='erpGoods',
            url="/api/auth/open/epaasJointLoginGyl",
            json={
                "eTicket": "JQing6",
                "serviceKey": "shop_goods"
            }
        ))
        return res.json()


class Request(Req):

    def __init__(self,
                 hostType: str = 'erp321',
                 callback: callable = None,
                 **kwargs
                 ):
        self.hostType = hostType
        self.callback = callback
        super().__init__(**kwargs)
