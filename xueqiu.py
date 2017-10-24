# coding: utf-8

import requests
import re
from const_value import headers, quote_API

def change_format(rawtime):
    monthes = { 'Jan' : '01',
                'Feb' : '02',
                'Mar' : '03',
                'Apr' : '04',
                'May' : '05',
                'Jun' : '06',
                'Jul' : '07',
                'Aug' : '08',
                'Sep' : '09',
                'Oct' : '10',
                'Nov' : '11',
                'Dec' : '12'}

    expr = r"\b(?P<week>\w\w\w)\s(?P<month>\w\w\w)\s(?P<date>\d\d)\s(?P<hour>\d\d):(?P<minute>\d\d):(?P<second>\d\d)\s(?P<zone>\D\d\d\d\d)\s(?P<year>\d\d\d\d)\b"
    x = re.search(expr, rawtime)

    return x.group('year')+'-'+monthes[x.group('month')]+'-'+x.group('date')+' '+x.group('hour')+':'+x.group('minute')+':'+x.group('second')

def quote(code):
    quote = {}
    try:
        r = requests.get(quote_API,
                        params={'code': code},
                        headers=headers,
                        timeout=10)
        if r.status_code == 200:
            quote['name'] = r.json()[code]['name']
            quote['price'] = r.json()[code]['current']
            quote['eps'] = r.json()[code]['eps']
            quote['pe_ttm'] = r.json()[code]['pe_ttm']
            quote['dividend'] = r.json()[code]['dividend']
            quote['net_assets'] = r.json()[code]['net_assets']
            quote['time'] = change_format(r.json()[code]['time'])
            return quote
        else:
            return r.json()['error_description']

    except requests.exceptions.RequestException as e:
        return e

# test
if __name__ == '__main__':
    try:
        while True:
            code = input("> ")
            result = quote(code)
            #content = u"%s，现价%s，每股盈利为%s，市盈率为%s，每股分红为%s，每股净资产为%s，更新时间%s。" %(result['name'], result['price'], result['eps'], result['pe_ttm'], result['dividend'], result['net_assets'], result['time'])
            print(result)
    except EOFError:
        print("Bye.")
