# 京东购物车下单
# 程序流程：全选购物车->确认订单->下单
# -*- coding=UTF-8 -*-
import time
import datetime
from tkinter import *
import tkinter.messagebox
import requests
import threading
import json

from api_pusher import send_message

ApiUrls = {
    'getProductInfos':
        'https://api.m.jd.com/api?functionId=pcCart_jc_getCurrentCart&appid=JDC_mall_cart&loginType=3&body={"serInfo":{"area":"13_1000_40488_54435","user-key":"78f2fbb3-610e-4057-bee3-eafe10da0f8f"},"cartExt":{"specialId":1}}',
    'addToCart':
        'https://cart.jd.com/gate.action?pid={pId}&pcount={count}&ptype=1',
    'getOrderInfo':
        'https://trade.jd.com/shopping/order/getOrderInfo.action?overseaMerge=1',
    'submitOrder':
        'https://trade.jd.com/shopping/order/submitOrder.action?overseaMerge=1&presaleStockSign=1&overseaPurchaseCookies=&vendorRemarks={vendorRemarks}&submitOrderParam.sopNotPutInvoice=true&submitOrderParam.trackID=TestTrackId&overseaMerge=1&submitOrderParam.ignorePriceChange=0&submitOrderParam.btSupport=0&submitOrderParam.eid=CH2AWTZNVCRPTFNPJQT2SZTJ5PSK7EV4TOQB7V5CCSVCUIOQ3K5ZT5S62PYV4V4YI4Z7EUXLNLKETTZBKFJ5J6WSO4&submitOrderParam.fp=33eaf773494fe391925ae6df450d557a&submitOrderParam.jxj=1',
    'checkAllOfCart': 'https://api.m.jd.com/api?functionId=pcCart_jc_cartCheckAll&appid=JDC_mall_cart&loginType=3'
}

cookies = {
    'shshshfpa': 'b73fcd0a-e748-3867-db73-a1a3173b9878-1532745038',
    'shshshfpb': '297f476594eaa487d83c7b4cb635aa1bd54b360e225a786a73afd6e3b0',
    '__jdu': '14990763208811196468013',
    'jcap_dvzw_fp': 'Dk6rZeuLxPLoJJsdAHum8XOefzbLrR1LCBMKdTBoazGSG4Tq6NcVM2LWQpG2Jty7j5Bg5g==',
    'whwswswws': '',
    'TARGET_UNIT': 'bjcenter',
    'ipLocation': '%u5c71%u4e1c',
    'PCSYCityID': 'CN_370000_370100_0',
    'unpl': 'JF8EAKZnNSttDUNRBhwFGhNCH1gEW10JTUQKaGANUwlcG1cNS1cbERZ7XlVdXhRKFx9ubhRUVVNOVg4eACsSEXtdVV9cCUkfBmZlNQkENh5VAEBYWyJLHm1XXm0ISicDam8NVVtfSVcEEgsbEhBDWlFZVAlLFTNfZw1QbWh7UgEeARsXEUNdZF9tCXtcbW4qBVFVUEpSAhkBGhsZS11UVloNTB4Cb2U1VW1b',
    'pinId': '1DFZEXqqCEKuTTSad7TecA',
    'pin': 'jd_sJovPmbhzNqJ',
    'unick': 'jd_sJovPmbhzNqJ',
    'ceshi3.com': '000',
    '_tp': '40NjtDUMie4wthDN5S8bNg%3D%3D',
    '_pst': 'jd_sJovPmbhzNqJ',
    'areaId': '26',
    'ipLoc-djd': '26-3970-3978-12253',
    '__jdv': '76161171|direct|-|none|-|1641819525010',
    '__jda': '122270672.14990763208811196468013.1499076321.1641812883.1641819525.414',
    '__jdc': '122270672',
    'wlfstk_smdl': 'b7576qtwl4jgrud2ca7a30jq81p1ufk5',
    'TrackID': '10TVO4Wf9dSeGDYvVRlx8gS0L4LZleGimD0i-Dq8LAYORMWG5Lb7RxuiKqy2bW3uxzPMCjYEURbx6WpH_JafgWaxLApZnMoXH2EA6uDmRqfgQl1XIvERh3oT9uTc-WfeW',
    'thor': 'CFBCF332498D096CCB7570306153F76A936F3D67B40701C976DACC6D49E33E49CD9EAC4BBE4ABB513A7B012D087F166CFF195EF51DD12D6C9BC3576ED222CCFD24BF2CE3FE753FB48A1E51E4EE2ADAC25D45988C143567C0C6B22734FC525C03D617550BE13D7D6787374D81BD09C75640D1AAB62B4D3C9D1103F391DB8217F71A44F8B53D9C025AC4A3294476A10A4C7035E6ED752D82D268165B090E035B8F',
    'shshshfp': '9062cc8a042ba9101c5c96af6c099085',
    '3AB9D23F7A4B3C9B': 'AYGPYJLVRTLAQIUTZ7I4JLRTE42V4DIV7BW6KSA5GYZCY3CL2ISYTJS3GHMR7VJZYMISFYV7NXSBSAIK3EN4CZR66Y',
    '__jdb': '122270672.5.14990763208811196468013|414.1641819525',
    'shshshsID': 'fc2750a3d5b55d3ea80de7980a551921_3_1641819598729',
    'cn': '0',
    'user-key': '78f2fbb3-610e-4057-bee3-eafe10da0f8f',
}


def getStrFromCookie(cookies):
    ck = ''
    for key in cookies:
        ck = ck + key + '=' + cookies[key] + ';'
    return ck


def make_app():
    app = Tk()
    app.geometry('800x550')
    app.title('京东加车抢')
    Label(app, text='cookie').place(relx=0.1, rely=0.05)
    cookieStr = StringVar()
    ck = getStrFromCookie(cookies)
    cookieStr.set(ck)
    Entry(app, textvariable=cookieStr, name='cookie').place(relx=0.1,
                                                            rely=0.1,
                                                            relwidth=0.8,
                                                            relheight=0.15)

    Label(app, text='输入抢单时间').place(relx=0.1, rely=0.3)
    timeStr = StringVar()
    timeStr.set(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    Entry(app, textvariable=timeStr, name='ipt').place(relx=0.1,
                                                       rely=0.35,
                                                       relwidth=0.3,
                                                       relheight=0.1)

    Label(app, text='商品ID').place(relx=0.45, rely=0.3)
    pId = StringVar()
    # pId.set('2148924,10026899941091,100013490678')  #
    pId.set('100031764590')  # sku
    Entry(app, textvariable=pId, name='ipt1').place(relx=0.45,
                                                    rely=0.35,
                                                    relwidth=0.2,
                                                    relheight=0.1)

    Label(app, text='数量').place(relx=0.7, rely=0.3)
    count = StringVar()
    count.set('1')
    Entry(app, textvariable=count, name='ipt2').place(relx=0.7,
                                                      rely=0.35,
                                                      relwidth=0.2,
                                                      relheight=0.1)

    Button(app, text='点击开始抢单', fg="black", bg="blue",
           command=orderThread).place(relx=0.1,
                                      rely=0.5,
                                      relwidth=0.8,
                                      relheight=0.1)

    Text(app, name="runningText").place(relx=0.1,
                                        rely=0.65,
                                        relwidth=0.8,
                                        relheight=0.3)
    runningText = app.children['runningText']
    runningText.insert(0.0, '\n抢单步骤：')
    runningText.insert(
        END,
        '\n第一步：网页登录京东，查看购物车下https://api.m.jd.com/api?functionId=pcCart_jc_getCurrentCart的cookie，填入cookie的输入框'
    )
    runningText.insert(END, '\n第二步：手动添加商品进购物车（注意限购数量），并将商品ID，填入商品ID输入框')

    return app


def orderThread():
    th = threading.Thread(target=checkCartAndSubmit)
    th.start()


def checkCartAndSubmit():
    cookie = app.children['cookie'].get()
    if cookie == '':
        tkinter.messagebox.showinfo(
            '错误',
            '请网页登录京东，查看购物车下https://api.m.jd.com/api?functionId=pcCart_jc_getCurrentCart的cookie，填入下面'
        )
        return

    # 全选购物车请求头
    checkCartHeaders = {
        'Cookie': cookie,
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'origin': 'https://cart.jd.com',
        'referer': 'https://cart.jd.com/',
        'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    }

    # 请求头
    tradeHeaders = {
        'Cookie': cookie,
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'path': '/shopping/order/submitOrder.action?',
        'origin': 'https://trade.jd.com',
        'referer': 'https://trade.jd.com/shopping/order/getOrderInfo.action',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'authority': 'trade.jd.com',
        'method': 'post',
        'scheme': 'https',
    }
    cartInfoheaders = {
        'Cookie': cookie,
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'origin': 'https://cart.jd.com',
        'referer': 'https://cart.jd.com',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'authority': 'api.m.jd.com',
        'method': 'post',
        'scheme': 'https',
    }

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    setTime = app.children['ipt'].get()
    # if now > setTime:
    #     tkinter.messagebox.showinfo('错误', '设置时间要超过当前时间')
    #     return

    # 轮询时间
    timeCut = 0.5

    pIds = app.children['ipt1'].get()
    # count = app.children['ipt2'].get()
    # 查询商品信息
    pInfoRes = requests.get(ApiUrls['getProductInfos'],
                            headers=cartInfoheaders, verify=False).json()
    vendors = []
    if (pInfoRes['success'] and pInfoRes['resultData']['cartInfo'] is not None):
        vendors = pInfoRes['resultData']['cartInfo']['vendors']
    else:
        tkinter.messagebox.showinfo('提示', '请把商品pIds加入购物车')

    vendorRemarks = []

    # 查找购买的商品的vendorId
    for vendor in vendors:
        for item in vendor['sorted']:
            if len(item['item']['items']) > 0:
                for iitem in item['item']['items']:
                    if pIds.find(str(iitem['item']['Id'])) > -1:
                        vendorRemarks.append({
                            "vendorId":
                                str(vendor['vendorId']),
                            "remark":
                                ""
                        })
                    break
            else:
                if pIds.find(str(item['item']['Id'])) > -1:
                    vendorRemarks.append({
                        "vendorId":
                            str(vendor['vendorId']),
                        "remark":
                            ""
                    })
                break

    for vendor in vendorRemarks:
        if vendor['vendorId'] == '8888':
            del vendorRemarks[vendorRemarks.index(vendor)]

    while True:
        runningText = app.children['runningText']

        currentTime = datetime.datetime.now()

        if currentTime.strftime('%Y-%m-%d %H:%M:%S.%f') >= setTime:

            for i in range(10):
                submitResult = reSubmitOrder(checkCartHeaders, tradeHeaders, vendorRemarks, runningText)
                if submitResult:
                    break
                runningText.insert(0.0, '\n第' + str(i) + '次抢单结束----' + datetime.datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S.%f'))
                time.sleep(0.5)

            break

        leftSec = (datetime.datetime.strptime(setTime, "%Y-%m-%d %H:%M:%S.%f") - currentTime).seconds
        runningText.insert(0.0, '\n倒计时：' + str(leftSec) + '秒------' + currentTime.strftime('%Y-%m-%d %H:%M:%S.%f'))
        if leftSec <= 1:
            time.sleep(0.1)
        else:
            time.sleep(timeCut)


def reSubmitOrder(checkCartHeaders, tradeHeaders, vendorRemarks, runningText):
    try:
        return _doSubmitOrder(checkCartHeaders, tradeHeaders, vendorRemarks, runningText)
    except Exception as e:
        runningText.insert(0.0, '\n程序异常：' + repr(e))

    # 默认false
    return False


def _doSubmitOrder(checkCartHeaders, tradeHeaders, vendorRemarks, runningText):

    # 全选购物车
    checkAllOfCartUrl = ApiUrls['checkAllOfCart']
    checkAllofCartRes = requests.get(checkAllOfCartUrl, headers=checkCartHeaders, verify=False)
    runningText.insert(0.0, '\n全选时间：' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    if checkAllofCartRes.json().get('resultData').get('cartInfo').get('checkedWareNum', 0) <= 0:
        return False
    # 确认订单
    getOrderInfoUrl = ApiUrls['getOrderInfo']
    getOrderInfoRes = requests.get(getOrderInfoUrl, headers=tradeHeaders, allow_redirects=False, verify=False)
    runningText.insert(0.0, '\n确认订单时间：' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    # 下单
    if getOrderInfoRes.status_code == 200:
        submitOrderUrl = ApiUrls['submitOrder'].format(vendorRemarks=json.dumps(vendorRemarks, separators=(',', ':')))
        submitOrderRes = requests.get(submitOrderUrl, headers=tradeHeaders, allow_redirects=False, verify=False)
        runningText.insert(0.0, '\n下单完成时间：' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        message = ''
        if submitOrderRes.json()['orderId'] != 0:
            message = '抢单成功'
            send_message(message)
            runningText.insert(0.0, '\n下单结果：' + message)
            return True
        else:
            message = submitOrderRes.json()['message']
            runningText.insert(0.0, '\n下单接口message：' + message)

    # 默认false
    return False


app = make_app()
app.mainloop()
