# coding: utf-8

import requests
import pandas as pd
from const_value import headers, lrb_API, fzb_API, llb_API

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
        with open(filename, 'wb') as f:
            f.write(r.content)
    except requests.exceptions.Timeout:
        return None

def download_fzb(code):
    try:
        r = requests.get(
            fzb_API, params={
            'page': 1,
            'size': 10000,
            'symbol': code,
            },
            headers=headers,
            timeout=5)
        filename = './data/report/' + code + '_fzb.csv'
        with open(filename, 'wb') as f:
            f.write(r.content)
    except requests.exceptions.Timeout:
        return None

def download_llb(code):
    try:
        r = requests.get(
            llb_API, params={
            'page': 1,
            'size': 10000,
            'symbol': code,
            },
            headers=headers,
            timeout=5)
        filename = './data/report/' + code + '_llb.csv'
        with open(filename, 'wb') as f:
            f.write(r.content)
    except requests.exceptions.Timeout:
        return None

def download_all(code):
    download_lrb(code)
    download_fzb(code)
    download_llb(code)
    return None

def get_lrb_data(code):
    lrb = pd.read_csv('./data/report/%s_lrb.csv' % (code),
                    encoding='utf-8',
                    header=0,
                    index_col=None)

    list_lrb = []
    for i in lrb[u'报表期截止日']:
        i_dt = str(i)[:4] + '-' + str(i)[4:6] + '-' + str(i)[6:8]
        list_lrb.append(i_dt)

    lrb['report_time'] = [pd.to_datetime(t) for t in list_lrb]

    lrb.index = lrb['report_time']

    lrb_data = lrb[::-1]

    return lrb_data

def get_fzb_data(code):
    fzb = pd.read_csv('./data/report/%s_fzb.csv' % (code),
                    encoding='utf-8',
                    header=0,
                    index_col=None)

    list_fzb = []
    for i in fzb[u'报表日期']:
        i_dt = str(i)[:4] + '-' + str(i)[4:6] + '-' + str(i)[6:8]
        list_fzb.append(i_dt)

    fzb['report_time'] = [pd.to_datetime(t) for t in list_fzb]

    fzb.index = fzb['report_time']

    fzb_data = fzb[::-1]

    return fzb_data

def get_llb_data(code):
    llb = pd.read_csv('./data/report/%s_llb.csv' % (code),
                    encoding='utf-8',
                    header=0,
                    index_col=None)

    list_llb = []
    for i in llb[u'报表期截止日']:
        i_dt = str(i)[:4] + '-' + str(i)[4:6] + '-' + str(i)[6:8]
        list_llb.append(i_dt)

    llb['report_time'] = [pd.to_datetime(t) for t in list_llb]

    llb.index = llb['report_time']

    llb_data = llb[::-1]

    return llb_data

def get_all_data(code):
    lrb_data = get_lrb_data(code)
    fzb_data = get_fzb_data(code)
    llb_data = get_llb_data(code)
    return lrb_data, fzb_data, llb_data

def get_data_month(data, month):
    return data[data.index.month == month]

def get_data_ratio(lrb_data, fzb_data, llb_data):
    result = pd.DataFrame()

    result['revenue'] = lrb_data[u'营业收入']
    result['net_profit'] = lrb_data[u'归属于母公司所有者的净利润']
    result['net_profit_ratio'] = lrb_data[u'归属于母公司所有者的净利润'] / lrb_data[u'营业收入']
    result['gross_profit_ratio'] = (lrb_data[u'营业收入'] - lrb_data[u'营业成本']) / lrb_data[u'营业收入']

    result['ROE'] = lrb_data[u'归属于母公司所有者的净利润'] / fzb_data[u'所有者权益(或股东权益)合计']

    result['GYXJL'] = llb_data[u'一、经营活动产生的现金流量净']
    result['GYXJL_profit_ratio'] = llb_data[u'一、经营活动产生的现金流量净'] / lrb_data[u'归属于母公司所有者的净利润']

    result.index = lrb_data['report_time']
    return result

def main(code):
    download_all(code)
    lrb_data, fzb_data, llb_data = get_all_data(code)
    result = get_data_ratio(lrb_data, fzb_data, llb_data)
    return result

if __name__ == '__main__':
    code = 'SH600900'
    report_time = '20161231'
    result = main(code)
    print(result.loc[report_time, 'ROE'])
