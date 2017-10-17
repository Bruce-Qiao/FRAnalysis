# coding: utf-8

import requests
from datetime import datetime
from const_value import xueqiu_cookie, quote_API, headers
from stocks import stocks

def quote(code):
    quote = {}
    try:
        r = requests.get(quote_API,
                        params={'code': code},
                        headers=headers,
                        timeout=5)

        print(r)
    except requests.exceptions:
        return ValueError

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
                print(content)
            elif code[0] in ['0', '3']:
                code = 'SZ' + code
                result = quote(code)
                content = u"%s，现价%s，每股盈利为%s，市盈率为%s，每股分红为%s，每股净资产为%s，更新时间%s。" %(result['name'], result['price'], result['eps'], result['pe_ttm'], result['dividend'], result['net_assets'], result['time'])
                #content = u"%s" % code
                print(content)
            else:
                content = u"输入的股票名称或代码有误！请重新输入。"
                print(content)
    except EOFError:
        print("Bye.")
