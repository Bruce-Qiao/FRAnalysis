# coding: utf-8

import re

def index():
    index = {}
    expr = r"(?P<code>\d\d\d\d\d\d)(?P<name>............)"

    with open('./data/code.txt', 'r') as f:
        content = f.read()

    for x in re.finditer(expr, content):
        index[x.groups()[1]] = x.groups()[0]

    with open('./data/stocks.py', 'wb') as stocks:
        for item in index.keys():
            stocks.write(("\'" + "%s" + "\'" + ": " + "\'" + "%s" + "\'" + "," + "\n") %(item, index[item]))

# test
if __name__ == '__main__':
    index()
