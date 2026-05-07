import time
import json
import re
import execjs
import requests
import os
import sys

# 设置 UTF-8 编码
sys.stdout.reconfigure(encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

# 获取当前脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


class Spider(object):
    def __init__(self):
        self.cookies = {
    "xlly_s": "1",
    "t": "7ecde91e5b40ef92216322d18c4ba092",
    "cna": "/Rd6IhuiAl0CAXBXPEyItZQR",
    "thw": "cn",
    "wk_cookie2": "1f393d388cdc183844b4fa1b1e587bef",
    "wk_unb": "UUphw2Qku4ZHwgL3iQ%3D%3D",
    "_hvn_lgc_": "0",
    "havana_lgc2_0": "eyJoaWQiOjIyMDkxNTYzOTc5MjUsInNnIjoiYTU5MWI4OTRmZDU4MGFkMGExYjhiYzAzZmFjNjQwZGYiLCJzaXRlIjowLCJ0b2tlbiI6IjFSX0h1WEFsQ1B5dmc4NlpoTVlNRm5BIn0",
    "lgc": "tb226337947",
    "dnk": "%5Cu67D2%5Cu96C5%5Cu7537%5Cu88C5%5Cu5E97",
    "tracknick": "tb226337947",
    "aui": "2209156397925",
    "cookie3_bak": "10ad88bbc44992364a49ea20dcdeaebe",
    "env_bak": "FM%2Bgm%2FLsIbXVPCLNH4oWKmj%2BtEsgrhImAUIH31sGPI2E",
    "cookie3_bak_exp": "1777973904330",
    "mtop_partitioned_detect": "1",
    "_m_h5_tk": "a3486890f6b26279cc66e84712a21b12_1777731116881",
    "_m_h5_tk_enc": "9e787a26fde791ed3327812fbe4bd23e",
    "hng": "CN%7Czh-CN%7CCNY%7C156",
    "_uetsid": "b3afd110462111f192fbcdf28f923791",
    "_uetvid": "b3afc5d0462111f1b5d7a52b031e6e4e",
    "_tb_token_": "b6be38b3e71e",
    "_samesite_flag_": "true",
    "cancelledSubSites": "empty",
    "havana_lgc_exp": "1808828638152",
    "sdkSilent": "1777753438151",
    "havana_sdkSilent": "1777753438151",
    "3PcFlag": "1777724638206",
    "fastSlient": "1777724638212",
    "cookie2": "2c626cf07d827d1b635aeefccbf4e73c",
    "sgcookie": "E100GBfpHdFmJAEUUt%2BwEQPRFuPqUlxWN2fX%2F0JUz7%2B0BEe4Cmn%2FLwiZZTGxANSL4bNKzBcz%2FiNACiDpXtnmXvrWlGYZbJnHW8C1WW6yfMioWzM%3D",
    "unb": "2209156397925",
    "uc1": "existShop=false&cookie16=URm48syIJ1yk0MX2J7mAAEhTuw%3D%3D&pas=0&cookie14=UoYZbY09Rx54rQ%3D%3D&cookie15=WqG3DMC9VAQiUQ%3D%3D&cookie21=WqG3DMC9Edo1SB5NB6Qtng%3D%3D",
    "uc3": "nk2=F5RHo33uJHlnW9E%3D&id2=UUphw2Qku4ZHwgL3iQ%3D%3D&lg2=URm48syIIVrSKA%3D%3D&vt3=F8dD1NBulFKd%2BwkNHag%3D",
    "csg": "d063f038",
    "cookie17": "UUphw2Qku4ZHwgL3iQ%3D%3D",
    "skt": "db9b950b2953d70e",
    "existShop": "MTc3NzcyNDY1Mg%3D%3D",
    "uc4": "id4=0%40U2grGNtqodshghf8z6thfM%2Bqf62%2FBfM9&nk4=0%40FY4MsTeJFvZghQd%2BVO50vr%2Bv5ygW7g%3D%3D",
    "_cc_": "W5iHLLyFfA%3D%3D",
    "_l_g_": "Ug%3D%3D",
    "sg": "75b",
    "_nk_": "tb226337947",
    "cookie1": "WvFdIvyfgRzlGja9uw3aKsyoJfEQavskwD2TTskP8zE%3D",
    "tfstk": "g-dqEa1vWjh49jmH8efZUHgPKJ5AN1oBnCs1SFYGlijclh1wQHI71qCjB1-N4hIfhsjb_CSk-VFjkxBGbnCcBKs1cG5wWHuSAXGBkECOnDiIOUpdxwfcoGbcIVflJNu5oJaHYYCOsDi7F5XxT1K4FMtAi8bl2NPcj1xGZUbGqN2cshjlEwbQm1fMj4ll8Na0mOxMr47OqGfGnhfozNIlj1fihetvXk_hnqkiiFw3D8sfxEjzsWzdut0J0RN0iA75hMXl450WaZWVxEAh8-udrQOPdTasp_YpFnbPTbwctUJMYpxtd8C2SKxOUnn8Ug9kMFjGnPVpze8DK_AsSyByqNWhsTzgsU5vU9RGtXqPyLYXIIK475bvGB6NvTug6O1kO9vH0P3prsbMX9dsvSIDSedpd6l7n6YyIHJN4urOr_3k6KrgQtbRzMgrzxHAqwtpouh8BRBlKaSIkO2TBtjlzMgrOReOHj7PAqvf.",
    "isg": "BE5OD1Raq0ykSB9ugfmsyUkenyQQzxLJHKvypHifC9EM2-Y14Ft-2XldFwe3Qwrh"
}
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Referer": "https://uland.taobao.com/sem/tbsearch",
            "Sec-Fetch-Dest": "script",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Google Chrome\";v=\"147\", \"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"147\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
           }
        self.url = "https://h5api.m.taobao.com/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0/"
        self._m_h5_tk = ''

    def get_token(self, keyword=""):
        # 通过JS生成请求参数
        js_file = os.path.join(SCRIPT_DIR, '分析.js')
        js_code = open(js_file, 'r', encoding='utf-8').read()
        js_params = execjs.compile(js_code).call('get_token_params', keyword)

        response = requests.get(
            self.url,
            params=js_params,
            cookies=self.cookies,
            headers=self.headers,
        )
        for cookie in response.cookies:
            self.cookies[cookie.name] = cookie.value
            if cookie.name == '_m_h5_tk':
                self._m_h5_tk = cookie.value
        print(f"Token已获取: {self._m_h5_tk}", file=sys.stderr)

    def get_data(self, page, keyword):
        token = self._m_h5_tk.split('_')[0]
        # 调用JS生成签名
        js_file = os.path.join(SCRIPT_DIR, '分析.js')
        js_code = open(js_file, 'r', encoding='utf-8').read()
        js_result = execjs.compile(js_code).call('get_sign', page, keyword, token)

        params = {
            'jsv': js_result['jsv'],
            'appKey': js_result['appKey'],
            't': js_result['t'],
            'sign': js_result['sign'],
            'api': 'mtop.relationrecommend.wirelessrecommend.recommend',
            'v': '2.0',
            'type': 'jsonp',
            'dataType': 'jsonp',
            'callback': 'mtopjsonp16',
            'data': js_result['data'],
        }

        response = requests.get(url=self.url, params=params, cookies=self.cookies, headers=self.headers)

        match = re.search(r'mtopjsonp16\((.*)\)', response.text)
        if not match:
            print(json.dumps({'code': -1, 'message': '解析失败'}))
            return

        jsonp_data = match.group(1)

        try:
            data_json = json.loads(jsonp_data)

            # 提取商品关键字段
            items = data_json.get('data', {}).get('itemsArray', [])
            product_list = []
            for item in items:
                product_list.append({
                    'pic_path': item.get('pic_path', ''),
                    'title': item.get('title', ''),
                    'price': item.get('price', ''),
                    'procity': item.get('procity', ''),
                    'realSales': item.get('realSales', ''),
                    'auctionURL': item.get('auctionURL', ''),
                })

            print(json.dumps({
                'code': 0,
                'message': 'success',
                'data': data_json,
                'products': product_list
            }, ensure_ascii=False))
        except json.JSONDecodeError as e:
            print(json.dumps({'code': -1, 'message': f'JSON解析失败: {e}'}))


if __name__ == '__main__':
    keyword = sys.argv[1] if len(sys.argv) > 1 else "相机"
    spider = Spider()
    spider.get_token()

    time.sleep(1)
    spider.get_data(1, keyword)
