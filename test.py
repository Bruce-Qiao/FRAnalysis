# coding: utf-8

import requests
import json
from const_value import xueqiu_login_data, xueqiu_cookie, API

#s = requests.session()
#s.post('http://www.xueqiu.com/login', xueqiu_login_data)

#lrb_base_url = 'http://api.xueqiu.com/stock/f10/incstatement.csv\?page\=1\&size\=10000\&symbol\='
#lrb_base_url = 'http://api.xueqiu.com/stock/f10/balsheet.csv\?symbol\=SH600900\&page\=1\&size\=10000'

cookie = {}

raw_cookies = 's=891cemiyal; bid=ae8beffa6c22afa52714f9be578d3c03_izyy0mys; webp=1; device_id=3cbcc3661371dbd737c5e8eff77088f0; aliyungf_tc=AQAAAHeGxkN0XwwAM9hQAdutSG+yFrE7; snbim_minify=true; remember=1; remember.sig=K4F3faYzmVuqC0iXIERCQf55g2Y; xq_a_token=551bf33159bfb2371188a999722fc89cdddb805d; xq_a_token.sig=0Nu_Ljzj6ACbbkQkHWjUYAPXLk4; xq_r_token=3485bed6b8fd77334ed869a8934e4088dffa3f5f; xq_r_token.sig=vjRsPLFVVRuFpqwsC0i5ckRBkSA; xq_is_login=1; xq_is_login.sig=J3LxgPVPUzbBg3Kee_PquUfih7Q; u=8193688136; u.sig=3fyT2DzG6-5xBt72u5TKuqyt1k0; __utmt=1; __utma=1.456128854.1488855348.1507685617.1507689404.16; __utmb=1.6.7.1507690089863; __utmc=1; __utmz=1.1507602659.11.4.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); Hm_lvt_1db88642e346389874251b5a1eded6e3=1507606065,1507606615,1507682617,1507688213; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1507690097'

for line in raw_cookies.split(';'):
    key, value = line.split('=', 1)
    cookie[key] = value

headers = {
    #'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #'Accept-Encoding':'gzip, deflate, br',
    #'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,ca;q=0.2,la;q=0.2',
    #'Cache-Control':'max-age=0',
    #'Connection':'keep-alive',
    #'Cookie':'s=891cemiyal; bid=ae8beffa6c22afa52714f9be578d3c03_izyy0mys; webp=1; device_id=3cbcc3661371dbd737c5e8eff77088f0; aliyungf_tc=AQAAAHeGxkN0XwwAM9hQAdutSG+yFrE7; snbim_minify=true; remember=1; remember.sig=K4F3faYzmVuqC0iXIERCQf55g2Y; xq_a_token.sig=0Nu_Ljzj6ACbbkQkHWjUYAPXLk4; xq_r_token.sig=vjRsPLFVVRuFpqwsC0i5ckRBkSA; xq_is_login.sig=J3LxgPVPUzbBg3Kee_PquUfih7Q; u.sig=3fyT2DzG6-5xBt72u5TKuqyt1k0; last_account=bruceq%40sina.com; __utma=1.456128854.1488855348.1507689404.1507692377.17; __utmb=1.4.10.1507692377; __utmc=1; __utmz=1.1507602659.11.4.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); Hm_lvt_1db88642e346389874251b5a1eded6e3=1507606065,1507606615,1507682617,1507688213; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1507693482; xq_a_token=551bf33159bfb2371188a999722fc89cdddb805d; xqat=551bf33159bfb2371188a999722fc89cdddb805d; xq_r_token=3485bed6b8fd77334ed869a8934e4088dffa3f5f; xq_is_login=1; u=8193688136; xq_token_expire=Sun%20Nov%2005%202017%2011%3A55%3A04%20GMT%2B0800%20(CST)',
    #'Host':'xueqiu.com',
    #'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }

url = 'https://xueqiu.com/S/SH600104/ZCFZB'
def download_lrb(code):
    #r = requests.get(url, headers=headers)
    try:
        r = requests.get(
            API, params={
            'page': 1,
            'size': 10000,
            'symbol': code
            },
            headers=headers,
            cookies=cookie,
            timeout=10)
        print(r.content.decode('utf-8'))
    except requests.exceptions.Timeout:
        return None

if __name__ == '__main__':
    download_lrb('600900')
