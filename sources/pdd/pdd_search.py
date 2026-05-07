import requests
import json
import time
import os
import subprocess
import sys

# 设置 UTF-8 编码
sys.stdout.reconfigure(encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

# 获取当前脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 可变参数 - 搜索关键词
KEYWORD = sys.argv[1] if len(sys.argv) > 1 else "相机"

# 设置 Node.js 编码
os.environ['NODE_SKIP_PLATFORM_CHECK'] = '1'

# 直接用 subprocess 执行 JS，绕过 execjs 的编码问题
def get_anti_content(timestamp):
    env_code = open(os.path.join(SCRIPT_DIR, 'env.js'), encoding="utf-8").read()
    pack_code = open(os.path.join(SCRIPT_DIR, 'pack.js'), encoding="utf-8").read()
    pack_code = pack_code.replace('require("./env")\n', '')
    # Node.js 中 global 未定义，需要 polyfill
    env_code = 'var global = global || {};\n' + env_code
    js_code = env_code + pack_code + f'\nconsole.log(get_anti_content({timestamp}))'

    # 写到临时文件执行，避免命令行长度限制
    tmp_file = os.path.join(SCRIPT_DIR, '_tmp.js')
    with open(tmp_file, 'w', encoding='utf-8') as f:
        f.write(js_code)

    result = subprocess.run(
        ['node', tmp_file],
        capture_output=True,
        text=False,
        cwd=SCRIPT_DIR
    )
    os.remove(tmp_file)
    stdout = result.stdout.decode('utf-8', errors='replace')
    stderr = result.stderr.decode('utf-8', errors='replace')
    if stderr:
        print("STDERR:", stderr)
    return stdout

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "anti-content": "0asAfxiygOXgygE2a4hp6YgUbF_Guw8gjP4ZDDDxaEVnFtoFgWKTqIddrQDDOOnuJWkrweEpaz-Nk0gV6V_SZAXVC_nA50w9q1tBU9CCggAsLnMEaw9bU0CkZkp7aGi3NHUaxSu90SbDwKsy85rB0xgH85Zl0x4m8VRVqiS1xEAgreIETPOS2giQguWy7yihgfIksPQd8CupAMV0uK9ZJKbZYDwiwXopwCxo6h49onNPnUp9NoThVhCPj-bzCAW40njN2FiTLOjXgHEIEm3ohClkRZ-gAEfibqoTQLDnXP_zUvpwFV2t85w4tcgfwlHSz7yyopIVGN-8gwGLGEeOCZhYv0a1RBKRda0_JGW-Djv7v3vZRzYnKcgld6UIwSI3oKNKStOk_Yeq5qIKQXKV_i7wnzkvq7xanLSoBOR_i25NWSHh5eGUGggBgcDcJghF7CjK_KHcc0Q48dvtiKRSBKsJKa0lsncGlltUcDimBQXAkZjAMp8mlmKIbRVJTL7xRvxcloRRSYuba6kMTrBxY5H5FZjnW-5z1V5ndgI6w5BhWZtPP1H5D6_vnl9PBWodf-tf4CrDkvDt0focj1SEDAI-TSdZqPao6XiC-K5M2LIyyyji7T-AHlMtvgSNs_PpxuoXizAvr0g8Roc537AlvTW-8dvEzRF8KTH_FLwi-FqtvB__yUHfjfVI_Q54skLlqNbb-J2P_L9lRGckaHhGbhs-feUC55K_jjqiKA3DBPTFrfiaw8098IQweLiwWRJWEd7zvdE3slrVAJzWRAPoRbZW7Zu5BaHe6cV8tmXqf39GxJzbc8vDGAz0lpNaM6uXijuRBj3Ncfm5C86PjSoYUU_5UkZ74YlqusEX2I1ZUW0NdZ7sS1gl4yU2rcZET66SFPN6nvEvc0U-0oGqr1n-KKaYxSPZ3EJKQ9a",
    "cache-control": "no-cache",
    "content-type": "application/json;charset=UTF-8",
    "origin": "https://mobile.yangkeduo.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://mobile.yangkeduo.com/search_result.html?search_key=%E7%89%9B%E5%A5%B6&search_met_track=history&search_type=goods&source=index&options=3&refer_search_met_pos=0&refer_page_el_sn=99887&refer_page_name=search_result&refer_page_id=10015_1778126352771_wxc82ekmp6&refer_page_sn=10015&page_id=10015_1778132591892_bjlauey3zn&is_back=&bsch_is_search_mall=&bsch_show_active_page=&list_id=l0jpd0b2iv&flip=0%3B0%3B0%3B0%3B077c73c6-a3a4-88a1-d93e-3d477f884b8e%3B%2F20%3B0%3B0%3Bcacde65970e1ecc6a1aa7a8c2f268612&sort_type=default&price_index=-1&filter=&opt_tag_name=&brand_tab_filter=",
    "sec-ch-ua": "\"Google Chrome\";v=\"147\", \"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"147\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
}
cookies = {
    "api_uid": "CkpSrWn7AM0LyQCufJyXAg==",
    "jrpl": "ITGUG8LvTHE8f3vypRNAoar6ZIcTw3FO",
    "njrpl": "ITGUG8LvTHE8f3vypRNAoar6ZIcTw3FO",
    "dilx": "9DkOwSHMgDLhUi59N5lRp",
    "webp": "1",
    "_nano_fp": "Xpm8l09ynqTqnqXonT_LyFd2EuJHD2QBEwbAoFQ6",
    "PDDAccessToken": "N3KVNPKRQDMWQQCOUCPAE3I2PMODKBQFA2KJK3ZR6GTXSY6B6XGQ121d745",
    "pdd_user_id": "2145958359",
    "pdd_user_uin": "SOQ3EL3OPYP4YQG3BAP2UPDBXU_GEXDA",
    "pdd_vds": "gaLxNnEtbsmynGEIEEQmOIilmLEwmOGtnsIwmbbmmoNIyLNlQmQLNlymOsEb"
}
url = "https://mobile.yangkeduo.com/proxy/api/search"
params = {
    "pdduid": "2145958359"
}
data = {
    "item_ver": "lzqq",
    "support_enhance_type": 1,
    "coupon_price_flag": 1,
    "source": "index",
    "search_met": "history",
    "track_data": "refer_page_id,10015_1778126352771_wxc82ekmp6;refer_search_met_pos,0",
    "list_id": "l0jpd0b2iv",
    "sort": "default",
    "filter": "",
    "q": KEYWORD,
    "page": 1,
    "is_new_query": 1,
    "size": 50,
    "flip": "0;0;0;0;077c73c6-a3a4-88a1-d93e-3d477f884b8e;/20;0;0;cacde65970e1ecc6a1aa7a8c2f268612",
    "anti_content": "0asAfxiygOXgygE2a4hp6YgUbF_Guw8gjP4ZDDDxaEVnFtoFgWKTqIddrQDDOOnuJWkrweEpaz-Nk0gV6V_SZAXVC_nA50w9q1tBU9CCggAsLnMEaw9bU0CkZkp7aGi3NHUaxSu90SbDwKsy85rB0xgH85Zl0x4m8VRVqiS1xEAgreIETPOS2giQguWy7yihgfIksPQd8CupAMV0uK9ZJKbZYDwiwXopwCxo6h49onNPnUp9NoThVhCPj-bzCAW40njN2FiTLOjXgHEIEm3ohClkRZ-gAEfibqoTQLDnXP_zUvpwFV2t85w4tcgfwlHSz7yyopIVGN-8gwGLGEeOCZhYv0a1RBKRda0_JGW-Djv7v3vZRzYnKcgld6UIwSI3oKNKStOk_Yeq5qIKQXKV_i7wnzkvq7xanLSoBOR_i25NWSHh5eGUGggBgcDcJghF7CjK_KHcc0Q48dvtiKRSBKsJKa0lsncGlltUcDimBQXAkZjAMp8mlmKIbRVJTL7xRvxcloRRSYuba6kMTrBxY5H5FZjnW-5z1V5ndgI6w5BhWZtPP1H5D6_vnl9PBWodf-tf4CrDkvDt0focj1SEDAI-TSdZqPao6XiC-K5M2LIyyyji7T-AHlMtvgSNs_PpxuoXizAvr0g8Roc537AlvTW-8dvEzRF8KTH_FLwi-FqtvB__yUHfjfVI_Q54skLlqNbb-J2P_L9lRGckaHhGbhs-feUC55K_jjqiKA3DBPTFrfiaw8098IQweLiwWRJWEd7zvdE3slrVAJzWRAPoRbZW7Zu5BaHe6cV8tmXqf39GxJzbc8vDGAz0lpNaM6uXijuRBj3Ncfm5C86PjSoYUU_5UkZ74YlqusEX2I1ZUW0NdZ7sS1gl4yU2rcZET66SFPN6nvEvc0U-0oGqr1n-KKaYxSPZ3EJKQ9a"
}
ts= int(time.time() * 1000)
result = get_anti_content(ts)

# 提取最后一行以0ar开头的字符串（anti_content）
lines = result.strip().split('\n')
anti = [l for l in lines if l.startswith('0a')][-1]

headers["anti_content"] = anti
data["anti_content"] = anti

data = json.dumps(data, separators=(',', ':'))
response = requests.post(url, headers=headers, cookies=cookies, params=params, data=data)

# 解析响应并提取商品列表
resp_json = response.json()

# 提取商品列表 (items -> item_data -> goods_model)
products = []
for item in resp_json.get('items', []):
    item_data = item.get('item_data', {})
    goods = item_data.get('goods_model', {})
    if goods:
        products.append({
            'goods_name': goods.get('goods_name', ''),
            'price': goods.get('price', 0) / 100,  # 价格单位是分
            'mall_name': goods.get('mall_name', ''),
            'sales': goods.get('sales', 0),
            'image_url': goods.get('thumb_url', '')
        })

result = {
    'code': 0,
    'total': resp_json.get('total', 0),
    'products': products
}
print(json.dumps(result, ensure_ascii=False))
