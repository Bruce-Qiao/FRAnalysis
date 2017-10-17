# coding: utf-8

from flask import Flask, request, make_response
import hashlib
import xml.etree.ElementTree as ET
import time
#from flask_sqlalchemy import SQLAlchemy

from const_value import weixin_token, quote_API, headers
from stocks import stocks
#from weather import query
from xueqiu import quote

def reply_txt(fromuser, touser, content):
    xml_reply = """
        <xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[%s]]></Content>
            <FuncFlag>0</FuncFlag>
        </xml>
                """

    response = make_response(xml_reply %(fromuser, touser, str(int(time.time())), content))
    response.content_type = 'application/xml'
    return response

def reply_img(fromuser, touser, mediaid):
    xml_reply = """
        <xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[image]]></MsgType>
            <Image>
            <MediaId><![CDATA[%s]]></MediaId>
            </Image>
            <FuncFlag>0</FuncFlag>
        </xml>
                """

    response = make_response(xml_reply %(fromuser, touser, str(int(time.time())), mediaid))
    response.content_type = 'application/xml'
    return response

app = Flask(__name__)

# create a database
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///weixindb'
# db = SQLAlchemy(app)
# class Weather(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     city = db.Column(db.String(40))
#     condition = db.Column(db.String(40))
#     temp = db.Column(db.String(20))
#     time = db.Column(db.String(80))
#     user = db.Column(db.String(120))
# db.create_all()

@app.route('/')
def index():
    return 'Flask is running!'

@app.route('/weixin', methods=['GET', 'POST'])
def weixin():
    if request.method == 'GET':
        if len(request.args) > 3:
            temparr = []
            token = weixin_token
            signature = request.args["signature"]
            timestamp = request.args["timestamp"]
            nonce = request.args["nonce"]
            echostr = request.args["echostr"]
            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            if hashcode == signature:
                return echostr
            else:
                return "Authorize failed!"
        else:
            return "Hello, this is handle view."
    else:
        webData = request.stream.read()
        xml_webData = ET.fromstring(webData)
        toUser = xml_webData.find('ToUserName').text
        fromUser = xml_webData.find('FromUserName').text
        input = xml_webData.find('Content').text

        if input == u"帮助":
            content = u"输入股票名称或代码查询股票信息。"
            return reply_txt(fromUser, toUser, content)
        elif input == u"历史":
            content = "开发中......"
            # list = Weather.query.filter_by(user=fromUser).all()
            # for item in list:
            #     content += u"%s，%s，温度为%s℃，更新时间%s。" %(item.city, item.condition, item.temp, item.time)
            return reply_txt(fromUser, toUser, content)
        elif u"你好" in input:
            mediaid = "zdPSAYy7F_xsTIsf9eG8bVCWQ6cM9a4RAfRPXpFlxWA5G-QiqOjw-RKQAwsaiaE-"
            return reply_img(fromUser, toUser, mediaid)
        # elif u"中秋快乐" in input:
        #     mediaid = "uwLYVopEPnC3IUDgdc2fWCiejvtn56p3z5hyI45bZspX7L6rFB3vaYQD2QsHGJaG"
        #     return reply_img(fromUser, toUser, mediaid)
        # elif input == u"笑话":
        #     content = u"不如你讲一个听听......"
        #     return reply_txt(fromUser, toUser, content)
        # elif input == u"美女":
        #     mediaid = "-HtO5H0Mh04ElazCAVkUdzgPXzcf_dFc1ZWoDR5csxNrKfWirKPvA5_CGp147mVv"
        #     return reply_img(fromUser, toUser, mediaid)
        # elif input == u"帅哥":
        #     mediaid = "WAgQ6DA7jA9EZKs_UCOpGMXqMDcKl-eJI2oPv6fwMUhua7HdKoF10ALIH3Rr7z72"
        #     return reply_img(fromUser, toUser, mediaid)
        else:
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

                # db.session.add(Weather(city=weather[0],
                #                         condition=weather[1],
                #                         temp=weather[2],
                #                         time=weather[3],
                #                         user=fromUser))
                # db.session.commit()
            return reply_txt(fromUser, toUser, content)

if __name__ == '__main__':
    app.run(debug = True)
