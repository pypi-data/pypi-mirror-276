import json
from erp_apis.erpRequest import Request, Session
from erp_apis.utils.util import getDefaultParams, JTable1


def shop_request(
        data: dict,
        method: str = 'LoadDataToJSON',
        url='app/daas/report/subject/adsorder/multidimension.aspx',
        callbackid: str = 'ACall1',
        **kwargs
) -> Request:
    params = getDefaultParams({'defaultParams': ["ts___", "_c"], 'am___': method})
    if kwargs.get('params'):
        params.update(kwargs.get('params'))
    print(params)
    return Request(
        method='POST',
        url=url,
        params=params,
        data={
            '__CALLBACKID': callbackid,
            **data
        },
        callback=JTable1
    )


def get_sale_data(data: dict = None, args: dict = None) -> Request:
    """
    获取店铺数据
    :param data: 回调参数
    :param args: 查询条件
    :return: 执行结果
    """
    # cfs = define_confs(sort)
    return shop_request(
        url=f'app/daas/report/subject/adsorder/multidimension.aspx',
        params={'___skutype': 'itemsku'},
        data={
            # 'search': json.dumps(search),
            'dataPageCount': '',
            # 'column_name': ['渠道', '日期'],
            '__CALLBACKPARAM': json.dumps(
                {"Method": "LoadDataToJSON", "Args": ["1", "", json.dumps(args)],
                 "CallControl": '{page}'}),
            **data,
        },
    )


def get_refund_data(data: dict = None, args: dict = None) -> Request:
    """
    获取店铺数据
    :param data: 回调参数
    :param args: 查询条件
    :return: 执行结果
    """
    # cfs = define_confs(sort)
    return shop_request(
        url=f'app/daas/report/subject/adsaftersale/multidimension.aspx',
        params={'___skutype': 'itemsku'},
        data={
            # 'search': json.dumps(search),
            'dataPageCount': '',
            # 'column_name': ['渠道', '日期'],
            '__CALLBACKPARAM': json.dumps(
                {"Method": "LoadDataToJSON", "Args": ["1", "", json.dumps(args)],
                 "CallControl": "{page}"}),
            **data,
        },
    )


# if __name__ == '__main__':
#     session = Session()
#     session.erpSend(login(
#         username="13264692157",
#         password="ZLjsb1266"
#     ))
#     data = {
#         'search': json.dumps([
#             {"k": "cost_type", "v": "0", "c": "@=", "t": ""},
#             {"k": "A.status", "v": "MERGED", "c": "!=", "t": ""},
#             {"k": "A.status", "v": "SPLIT", "c": "!=", "t": ""},
#             {"k": "combinesku_type", "v": 2, "c": "@=", "t": ""},
#             {"k": "A.pay_date", "v": "昨天", "c": ">=", "t": "date"},
#             {"k": "A.pay_date", "v": "昨天 23:59:59.999", "c": "<=", "t": "date"}]),
#         'column_name': ['渠道', '日期'],
#     }
#     args = {
#         'args': {"fld": "销售数量", "type": "desc"},
#     }
#     res = session.erpSend(get_sale_data(data=data, args=args))
#     print(res.json())
