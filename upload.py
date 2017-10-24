# coding: UTF-8
# filename: upload.py
import requests
import time

from const_value import AppID, AppSecret

class Basic(object):
    def __init__(self):
        self.__accessToken = ''
        self.__leftTime = 0
    def __real_get_access_token(self):
        postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type="
               "client_credential&appid=%s&secret=%s" % (AppID, AppSecret))
        urlResp = requests.post(postUrl)
        urlResp = urlResp.json()

        self.__accessToken = urlResp['access_token']
        self.__leftTime = urlResp['expires_in']

    def get_access_token(self):
        if self.__leftTime < 10:
            self.__real_get_access_token()
        return self.__accessToken

    def run(self):
        while(True):
            if self.__leftTime > 10:
                time.sleep(2)
                self.__leftTime -= 2
            else:
                self.__real_get_access_token()

def upload_pic(filename):
    basic = Basic()
    access_token = basic.get_access_token()

    postUrl = ("https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=image" % access_token)
    urlResp = requests.post(postUrl, files={'file': open(filename, 'rb')})
    return urlResp.json()['media_id']

if __name__ == '__main__':
    print(upload_pic('./data/pic/SH600900_revenue.jpg'))
