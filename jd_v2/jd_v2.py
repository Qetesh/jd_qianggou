# 京东购物车下单
# 程序流程：全选购物车->确认订单->下单
# -*- coding=UTF-8 -*-
import datetime
import json
import threading
import time
import tkinter.messagebox
from tkinter import *

import requests

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
    'unpl': 'JF8EAKZnNSttDUNRBhwFGhNCH1gEW10JTUQKaGANUwlcG1cNS1cbERZ7XlVdXhRKFx9ubhRUVVNOVg4eACsSEXtdVV9cCUkfBmZlNQkENh5VAEBYWyJLHm1XXm0ISicDam8NVVtfSVcEEgsbEhBDWlFZVAlLFTNfZw1QbWh7UgEeARsXEUNdZF9tCXtcbW4qBVFVUEpSAhkBGhsZS11UVloNTB4Cb2U1VW1b',
    'pinId': '1DFZEXqqCEKuTTSad7TecA',
    'pin': 'jd_sJovPmbhzNqJ',
    'unick': 'jd_sJovPmbhzNqJ',
    'ceshi3.com': '000',
    '_tp': '40NjtDUMie4wthDN5S8bNg%3D%3D',
    '_pst': 'jd_sJovPmbhzNqJ',
    '__jdv': '76161171|direct|-|none|-|1641819525010',
    'areaId': '13',
    'ipLoc-djd': '13-2900-2908-0',
    '__jdc': '122270672',
    'wlfstk_smdl': '34pcp29gasywa4lrqc4ayj1yzbv4vo3z',
    'TrackID': '1NjJ4WcCUrxLirF1mPiMYyEVZjHiABe532lTjbn2TLxdpCOgAbrNm1PoNr0x3v1Zp81FjDrU6YlM0XVki340gvceVOUet7-9tTyD0oE4gM82JAoJT12JFmOHqQzbiM2OP',
    'shshshfp': 'f7ce069b6da41cf4cc77ef6104dd13f8',
    '3AB9D23F7A4B3C9B': 'AYGPYJLVRTLAQIUTZ7I4JLRTE42V4DIV7BW6KSA5GYZCY3CL2ISYTJS3GHMR7VJZYMISFYV7NXSBSAIK3EN4CZR66Y',
    'thor': 'CFBCF332498D096CCB7570306153F76A936F3D67B40701C976DACC6D49E33E499297D8CA75C5602E01DE77777AFD73B979798879EDA91366D4CF2A258BC08AE6EA69F9E8C57ECFCB1B00CB0F118EB53F5872E7BE47C2FBC15FCA3F24988E1695C865A3C022C1F513E7F6C9BD879653A0EAA94B6D6B8091064FCFF9CCD2587496FA601F389CEAEE634BFC5EE7EAC599791A3C2927484B65DB170244DB1FD52B1A',
    '__jda': '122270672.14990763208811196468013.1499076321.1642242982.1642246687.420',
    '__jdb': '122270672.1.14990763208811196468013|420.1642246687',
    'shshshsID': '9f43f829f9f9c6d95b2d7dd89e22f48f_1_1642246687210',
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
    app.geometry('600x450')
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
    pId.set('100019743172')  # sku
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

    Button(app, text='点击开始抢单', fg="black", bg="white",
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
    s = requests.Session()
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
    pInfoRes = s.get(ApiUrls['getProductInfos'],
                     headers=cartInfoheaders, verify=False).json()
    vendors = []
    if pInfoRes['success'] and pInfoRes['resultData']['cartInfo'] is not None:
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

            for i in range(3):
                submitResult = reSubmitOrder(s, checkCartHeaders, tradeHeaders, vendorRemarks, runningText)
                if submitResult:
                    break
                runningText.insert(0.0, '\n第' + str(i) + '次抢单结束----' + datetime.datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S.%f'))
                time.sleep(0.1)

            break

        leftSec = (datetime.datetime.strptime(setTime, "%Y-%m-%d %H:%M:%S.%f") - currentTime).seconds
        runningText.insert(0.0, '\n倒计时：' + str(leftSec) + '秒------' + currentTime.strftime('%Y-%m-%d %H:%M:%S.%f'))
        if leftSec <= 1:
            time.sleep(0.05)
        else:
            time.sleep(timeCut)


def reSubmitOrder(s, checkCartHeaders, tradeHeaders, vendorRemarks, runningText):
    try:
        return _doSubmitOrder(s, checkCartHeaders, tradeHeaders, vendorRemarks, runningText)
    except Exception as e:
        runningText.insert(0.0, '\n程序异常：' + repr(e))

    # 默认false
    return False


def _doSubmitOrder(s, checkCartHeaders, tradeHeaders, vendorRemarks, runningText):
    start_time = int(datetime.datetime.now().timestamp() * 1000)

    # 全选购物车
    checkAllOfCartUrl = ApiUrls['checkAllOfCart']
    checkAllofCartRes = s.get(checkAllOfCartUrl, headers=checkCartHeaders, verify=False)
    if checkAllofCartRes.json().get('resultData').get('cartInfo').get('checkedWareNum', 0) <= 0:
        return False

    # 确认订单
    getOrderInfoUrl = ApiUrls['getOrderInfo']
    getOrderInfoRes = s.get(getOrderInfoUrl, headers=tradeHeaders, allow_redirects=False, verify=False)
    # runningText.insert(0.0, '\n确认订单时间：' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))

    # 下单
    if getOrderInfoRes.status_code == 200:
        submitOrderUrl = ApiUrls['submitOrder'].format(vendorRemarks=json.dumps(vendorRemarks, separators=(',', ':')))
        submitOrderRes = s.get(submitOrderUrl, headers=tradeHeaders, allow_redirects=False, verify=False)
        runningText.insert(0.0, '\n下单完成时间：' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        message = ''
        if submitOrderRes.json()['orderId'] != 0:
            message = '抢单成功'
            runningText.insert(0.0, '\n下单结果：' + message)
            return True
        else:
            message = submitOrderRes.json()['message']
            runningText.insert(0.0, '\n下单接口message：' + message)

    end_time = int(datetime.datetime.now().timestamp() * 1000)

    print('diff=' + str(end_time - start_time))
    # 默认false
    return False


app = make_app()
app.mainloop()
