import subprocess
import json
import requests
import re
import os
import sys
from urllib.parse import quote

# 设置 UTF-8 编码
sys.stdout.reconfigure(encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

# 获取当前脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


# 需要提取的字段
EXTRACT_FIELDS = [
    'imageurl', 'sellingPoint', 'wareId', 'wareName',
    'shopId', 'shopName', 'oriPrice', 'realPrice',
    'totalSales', 'commentFuzzy', 'averageScore'
]


def extract_products(raw_response):
    """从京东搜索响应中提取关键字段"""
    extracted = []
    ware_list = raw_response.get('data', {}).get('wareList', [])
    for item in ware_list:
        record = {}
        for field in EXTRACT_FIELDS:
            val = item.get(field, '')
            if field == 'sellingPoint' and isinstance(val, list):
                val = ' | '.join(val)
            if field == 'imageurl' and val:
                val = 'https://img14.360buyimg.com/n1/' + val
            if field == 'wareName' and val:
                val = re.sub(r'<[^>]+>', '', val)
            record[field] = val if val is not None else ''
        extracted.append(record)
    return extracted


def get_h5st_params(keyword, page=1):
    """调用 produre.js 生成 h5st 参数"""

    # 运行 produre.js 直接获取 h5st
    result = subprocess.run(
        ['node', 'produre.js'],
        cwd=SCRIPT_DIR,
        capture_output=True,
        text=True,
        encoding='utf-8'
    )

    # 从输出中提取 h5st 结果
    output = result.stdout

    # 从输出中用正则提取关键字段
    h5st_match = re.search(r"h5st: '([^']+)'", output)
    t_match = re.search(r"t: (\d+)", output)
    body_match = re.search(r"body: '([^']+)'", output)
    functionId_match = re.search(r"functionId: '([^']+)'", output)

    if h5st_match:
        return {
            "h5st": h5st_match.group(1),
            "t": t_match.group(1) if t_match else "",
            "body": body_match.group(1) if body_match else "",
            "functionId": functionId_match.group(1) if functionId_match else "pc_search_searchWare",
            "appid": "search-pc-java",
            "client": "pc",
            "clientVersion": "1.0.0"
        }

    print("解析失败，输出:", output[:500] if output else "空输出")
    raise ValueError("无法从 produre.js 获取 h5st")


def search_jd(keyword, page=1):
    """搜索京东 - 使用 subprocess 调用 curl"""

    # 获取 h5st 参数
    params = get_h5st_params(keyword, page)

    # URL 参数
    url = "https://api.m.jd.com/api"

    cookies = 'jcap_dvzw_fp=WqXUjVGKP786dcmi8i3cSEewzOwKE6tr95YI-XFGF2znP2MlSDIEBTzwyxNHSgVZ3fcVUHjVIz4wq3kc4nG8ng==; __jdu=17653516403361429620305; b_webp=1; b_avif=1; shshshfpa=3be41945-8252-fd44-289f-bca9f2f0a526-1765437213; shshshfpx=3be41945-8252-fd44-289f-bca9f2f0a526-1765437213; b_dpr=1.25; b_dw=1484; autoOpenApp_downCloseDate_auto=1775627825074_1800000; b_dh=942; __jdv=76161171|www.bing.com|-|referral|-|1778041060033; PCSYCityID=CN_320000_320100_0; umc_count=1; wlfstk_smdl=hoqlq74v36n6ipsu8vpba6o50lplwz1d; TrackID=1AdBruJMaX6hE98_Gp7bsT26VZCJbQgYl3E39vbgi9vrJsPofKpYu5JaU-mng76R8aflLx4iKqBzRL0hiQTG2gGFNB44MXlpFdKQWDRIbrwk; thor=577683CAB1CB3027F553E9FF17A93FE2F4432CBD22C4880D1791C4827AC8FF085B5CCB1C3EFA4DC2D70E5766CF1E3B27097B117CC9A51669D945D2109B70CF14F84BB58CC221729323FE356C4E408E56289F742CC7E76BE2B469A560411E277193970F1C40008BEE77024691E3872F7A5C1587124849CF5C347AAC9622A47254CB6BE7EA15FEFF52816A733DAAFD7B10E425DBC76E3288961FF9C45AF2C9DFAA; light_key=AASBKE7rOxgWQziEhC_QY6yaIgCevEgT_iNSL9ppfmsdR-ez6NNIIhJChbxMuNWOANHqjxoj; pinId=hPPMeqA0GhgVcdbTpPSIbA; pin=jd_xbHQlKpnrCSP; unick=2e034k4t79i29j; ceshi3.com=000; _tp=gmY4SC0T%2FGcxJ77BnIgAWw%3D%3D; _pst=jd_xbHQlKpnrCSP; cn=0; PCSYHWHR=0; areaId=1; ipLoc-djd=1-72-55652-0; mail_times=4%2C2%2C1778053040842; __jda=143920055.17653516403361429620305.1765351640.1778046889.1778051488.23; __jdc=143920055; flash=3_tmQ0bVeS-yPs8fIVn7QauM53_5KNBxRyQg363HL0rFKKEIDG4EvCZ3TTt3EcSc8gL8uDUU6G8gami8QkP8-5XnfteZmV4PQOQAmIOVvsNDVVG3i3kR2gWFtvLC6uy_80pBP-bjPPrBEel-YrTBvQP0NLnvcflaCgn4LRu1Eyj3LLEFkquGhW; __jdb=143920055.71.17653516403361429620305|23.1778051488; 3AB9D23F7A4B3CSS=jdd03PXST65TQFULZR5TMTB6SGEGYRRESUQC3LPFEI4PQIODCCF7YUGNGCYZ5DXY32NYKXGDN6UQII4BQMTXH3PDTOJEH3IAAAAM57Q4T37YAAAAADISWBV4YDF77LQX; _gia_d=1; cid=9; shshshfpb=BApXWrNEx__hAErdVcBUT8JpW1d5JNhT8BicCdTxo9xJ1PdZfQp7Uuivnpzv0IaVAQwIY76jnsaxhJro9uqta5tkuMVuwqA-J5cc; 3AB9D23F7A4B3C9B=PXST65TQFULZR5TMTB6SGEGYRRESUQC3LPFEI4PQIODCCF7YUGNGCYZ5DXY32NYKXGDN6UQII4BQMTXH3PDTOJEH3I; sdtoken=AAbEsBpEIOVjqTAKCQtvQu17Zih3V6bZ1cexRc0jU6evGvq-woFY0WftX6Yp0Bo7oiOy7DHE4wFRdVcLtx9bN3lV3TRWBVAF7BDbFE5Kt8uf6I16L8sBYloHMTBotw2CGiYG6coJF0rxuNIuUm8HnZz13fvjboaGXeRAUZmCzSxVhtXy4Hk'

    # 构建 curl 命令
    import urllib.parse
    query_string = urllib.parse.urlencode({
        "appid": params.get("appid", "search-pc-java"),
        "t": params.get("t", ""),
        "client": params.get("client", "pc"),
        "clientVersion": params.get("clientVersion", "1.0.0"),
        "cthr": "1",
        "uuid": "1775621939231919443843",
        "loginType": "3",
        "keyword": keyword,
        "functionId": params.get("functionId", "pc_search_searchWare"),
        "body": params.get("body", ""),
        "x-api-eid-token": "jdd03VMPW45O47R4DCZH6XHAIYONDVAQ23SIGFNEJWJ227GM2RUGIF6JCF623EUZ753IUISMTG5LQZID2TORAIRCV24AQ7MAAAAM57QLI7WYAAAAADA3MO7CYHNNVSMX",
        "h5st": params.get("h5st", ""),
    })

    curl_cmd = f'''curl -s "{url}?{query_string}" '''
    curl_cmd += f'''-H "accept: application/json, text/plain, */*" '''
    curl_cmd += f'''-H "accept-language: zh-CN,zh;q=0.9" '''
    curl_cmd += f'''-H "cache-control: no-cache" '''
    curl_cmd += f'''-H "cookie: {cookies}" '''
    curl_cmd += f'''-H "origin: https://search.jd.com" '''
    curl_cmd += f'''-H "pragma: no-cache" '''
    curl_cmd += f'''-H "priority: u=1, i" '''
    curl_cmd += f'''-H "referer: https://search.jd.com/Search?keyword=%E7%9B%B8%E6%9C%BA&enc=utf-8" '''
    curl_cmd += f'''-H 'sec-ch-ua: "Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"' '''
    curl_cmd += f'''-H "sec-ch-ua-mobile: ?0" '''
    curl_cmd += f'''-H "sec-ch-ua-platform: \\"Windows\\"" '''
    curl_cmd += f'''-H "sec-fetch-dest: empty" '''
    curl_cmd += f'''-H "sec-fetch-mode: cors" '''
    curl_cmd += f'''-H "sec-fetch-site: same-site" '''
    curl_cmd += f'''-H "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36" '''
    curl_cmd += f'''-H "x-referer-page: https://search.jd.com/Search" '''
    curl_cmd += f'''-H "x-rp-client: h5_2.0.0"'''

    # 执行 curl
    result = subprocess.run(curl_cmd, shell=True, capture_output=True)

    if result.stdout:
        try:
            # Windows 下是 GBK 编码，需要解码
            text = result.stdout.decode('utf-8', errors='ignore')
            return json.loads(text)
        except json.JSONDecodeError:
            print(f"响应内容: {result.stdout[:500]}")
            return None
    else:
        print(f"错误: {result.stderr}")
        return None


if __name__ == "__main__":
    import sys
    keyword = sys.argv[1] if len(sys.argv) > 1 else "相机"
    result = search_jd(keyword)
    if result:
        extracted = extract_products(result)
        print(json.dumps({
            'code': result.get('code'),
            'message': result.get('message', ''),
            'data': result.get('data', {}),
            'extracted': extracted
        }, ensure_ascii=False))
    else:
        print(json.dumps({'code': -1, 'message': '搜索失败'}))
