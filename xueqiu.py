# coding: utf-8

import requests
import re
from datetime import datetime
from const_value import headers, quote_API
from stocks import stocks

def quote(code):
    quote = {}
    try:
        r = requests.get(quote_API,
                        params={'code': code},
                        headers=headers,
                        timeout=5)
        quote['name'] = r.json()[code]['name']
        quote['price'] = r.json()[code]['current']
        quote['eps'] = r.json()[code]['eps']
        quote['pe_ttm'] = r.json()[code]['pe_ttm']
        quote['dividend'] = r.json()[code]['dividend']
        quote['net_assets'] = r.json()[code]['net_assets']
        quote['time'] = r.json()[code]['time']
        content = u"%s, %s" %(quote['name'], quote['price'])
        #print(content)
        return quote
    except requests.exceptions.Timeout:
        return None
# test
if __name__ == '__main__':
    try:
        while True:
            input = raw_input("> ")
            code = input
            for item in stocks.keys():
                if input == item:
                    code = stocks[item]
            if code[0] == '6':
                code = 'SH' + code
                result = quote(code)
                content = u"%s，现价%s，每股盈利为%s，市盈率为%s，每股分红为%s，每股净资产为%s，更新时间%s。" %(result['name'], result['price'], result['eps'], result['pe_ttm'], result['dividend'], result['net_assets'], result['time'])
                #content = u"%s" % code
            elif code[0] in ['0', '3']:
                code = 'SZ' + code
                result = quote(code)
                content = u"%s，现价%s，每股盈利为%s，市盈率为%s，每股分红为%s，每股净资产为%s，更新时间%s。" %(result['name'], result['price'], result['eps'], result['pe_ttm'], result['dividend'], result['net_assets'], result['time'])
                #content = u"%s" % code
            else:
                content = u"输入的股票名称或代码有误！请重新输入。"
            print(content)
    except EOFError:
        print("Bye.")
