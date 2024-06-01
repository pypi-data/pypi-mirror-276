# wss连接
import asyncio, json, websockets, requests


async def connect_print(wss_url):
    return await websockets.connect(wss_url)


class PrintAssistant:
    def __init__(self, wss_url='wss://localhost:13529/'):
        self.new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.new_loop)
        self.client = self.new_loop.run_until_complete(connect_print(wss_url))

    def send_print(self, msg):
        return self.new_loop.run_until_complete(self.__send__(msg))

    async def __send__(self, msg):
        await self.client.send(json.dumps(msg))
        while self.client.open:
            response = json.loads(await self.client.recv())
            return response


def getPrintTemplate(skus):
    data = {
        'type': 'tags',
        'sub_type': 'jm',
        'skus': json.dumps(skus),
        'moudle': 'AS',
        'preview': 'false',
        'debugger': 'false',
    }
    res = requests.post(
        url="https://www.erp321.com/app/print/print/Printer.aspx?async=true&ts___=1716971834507",
        headers={
            'Cookie': '_ati=661673026695; 3AB9D23F7A4B3C9B=T7KGM6ENOCUV5EU75WFUERLH67V76R3MRBOQACP7W7S6Q6USAE4SVS7Q3A6TKSXNLYVCDDHSOF5FA2PLSML4QSXRFM; u_name=%e6%9d%8e%e7%a6%8f%e6%88%90; u_lid=18986680202; j_d_3=T7KGM6ENOCUV5EU75WFUERLH67V76R3MRBOQACP7W7S6Q6USAE4SVS7Q3A6TKSXNLYVCDDHSOF5FA2PLSML4QSXRFM; u_ssi=; u_co_name=%e6%ad%a6%e6%b1%89%e5%b0%8f%e5%b8%83%e7%94%b5%e5%ad%90%e5%95%86%e5%8a%a1%e6%9c%89%e9%99%90%e5%85%ac%e5%8f%b8; u_drp=; v_d_144=1716701921846_f03bbc877f72bd4604a698ddf069f641; u_cid=133611755328139780; u_r=12%2c13%2c14%2c15%2c17%2c18%2c22%2c23%2c27%2c28%2c29%2c30%2c31%2c32%2c33%2c34%2c35%2c36%2c39%2c40%2c41%2c52%2c53%2c54%2c61%2c62%2c101%2c1001%2c109; u_sso_token=CS@db3f54c6f3dc4d4b9928a86c5c86856e; u_id=15424700; u_shop=-1; u_co_id=10174711; p_50=D2A0B7B0332756A4BB135A9FDD6660AF638523275328143166%7c10174711; u_env=www; u_lastLoginType=ap; SessionCode=299f533b-d49e-9a89-0a6418fb3957208; combine_show=true; jt.pagesize=.-E3E1ZS._500; order_filter15424700=sl_.oql_.sl_agreement.bml_.rl_.date_arrow.iteml_.referr_.sourceStore_.other_-wor_co_id_to__.ssl_.nodesl_.ofl_.presend_head.tl_.icl_.labels_title.st_.p_shops_title.drp_co_id_tos_title.ll_.rl__.l_status_label.wh_.lwh_.asl__.customer_; u_json=%7b%22t%22%3a%222024-5-28+15%3a44%3a40%22%2c%22co_type%22%3a%22%e6%a0%87%e5%87%86%e5%95%86%e5%ae%b6%22%2c%22proxy%22%3anull%2c%22ug_id%22%3a%2211003725%22%2c%22dbc%22%3a%221149%22%2c%22tt%22%3a%2295%22%2c%22apps%22%3a%221.4.7.150.152.168.169%22%2c%22pwd_valid%22%3a%220%22%2c%22ssi%22%3a%22%22%2c%22sign%22%3a%224017121.7DDBD535E7E14FEABF8D0ACC7BC80C7F%2c7d6a3981589f28bc02722ad2b68e01fc%22%7d; 15424700ckv=%7B%22order-info%22%3A%22true%22%2C%22pay-info%22%3A%22false%22%2C%22receiver-info%22%3A%22false%22%2C%22orderItem-info%22%3A%22false%22%7D; ckv=%7B%22itemsku_defaultFillQtyReturns%22%3Atrue%2C%22setwarehouse_clearlc%22%3A%22default%22%2C%22warehouseScaleEnabled%22%3Afalse%7D; dkv=%7B%22pstol_item%22%3A%220%2C0%22%2C%22pstorder_editor%22%3A%22-155%2C-87%22%7D; acw_tc=2760827917169706931404769e2b7e82d0b06d5717ff8a763b5cd518022cb5; tfstk=fYnE6cXR3HKE3W0u_5Zz_KXolpZpNuleGMo7E8D-eTV3xM1lZ5l4F7N3rl0ZZfUQt0kR48DowpFWpFMKpuEkGIGycvHLKuE4c0z3Sh2SI62uKdV3SrrkGIt_wa7GOu05ym6_bAVTU623ZbxiI5e5-7cutPfg3-EuZbqkQN2bLMfuZybGIbjtZXIa_yApdzFQhw_Gg5k3_ik9sJ4hcc_SIAoaLyP0S5SkEcyU8SDnvUgHZRmsbra1FBriHVG3Qo-1-oDZrjumwE_TYY0nwPlp6NPsSVMoYPWR2jrEarm37TjzYkP3bRmDFZFsbWGoYPvf0zZicrqn5FdQPkyqZDhFUgcmCxiLW0RVs73QHl2jpHSamv2l4U58Io4s225lry2TQS9wI__NvtTP_b2OyaUwWRPXHKQRyy43QS9MjaQ8SseaGKSF.',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36 Edg/106.0.1370.42',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        },
        data=data
    )
    return res.json().get('requestBodys')[0]


if __name__ == '__main__':
    skus = [
        {
            "sku_id": "L-男宽松T-深灰-想法棕-CP",
            "qty": 1,
            "co_id": 10174711,
            "as_id": 1452928491,
            "so_id": "3909832416880161727",
            "shop_id": "10264796",
            "question_type": "拍错/多拍/不喜欢",
            "AsRemark": "",
            "AsDetailRemark": "",
            "i_id": "XBZM19BT01",
            "owner_co_id": 0,
            "o_id": 40981215,
            "pay_date": "2024-05-29 16:00:17"
        }
    ]

    temp = getPrintTemplate(skus)
    p = PrintAssistant()
    res = p.send_print(temp)
    print(res)
