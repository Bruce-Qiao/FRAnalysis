# coding: utf-8

import requests
from const_value import xueqiu_cookie, quote_API
from index import index

headers = {
    'User-Agent': 'Mozilla/5.0',
    'Cookie': xueqiu_cookie
    }

def quote(code):
    quote = {}
    try:
        r = requests.get(quote_API,
                        params={'code': code},
                        headers=headers,
                        timeout=5)
        quote['name'] = r.json()[code]['name']
        quote['current_price'] = r.json()[code]['current']
        quote['eps'] = r.json()[code]['eps']
        quote['pe_ttm'] = r.json()[code]['pe_ttm']
        quote['dividend'] = r.json()[code]['dividend']
        quote['net_assets'] = r.json()[code]['net_assets']
        return quote
    except requests.exceptions.Timeout:
        return None

if __name__ == '__main__':
    quote('SH600900')
