# coding: utf-8

import requests
from const_value import xueqiu_cookie, lrb_API

headers = {
    'User-Agent': 'Mozilla/5.0',
    'Cookie': xueqiu_cookie
    }

def download_lrb(code):
    try:
        r = requests.get(
            lrb_API, params={
            'page': 1,
            'size': 10000,
            'symbol': code,
            },
            headers=headers,
            timeout=5)
        filename = './data/report/' + code + '_lrb.csv'
        print(filename)
        with open(filename, 'wb') as f:
            f.write(r.content)
    except requests.exceptions.Timeout:
        return None

if __name__ == '__main__':
    download_lrb('SH601088')
