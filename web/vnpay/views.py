import hashlib
import hmac
import urllib
import urllib.parse
import urllib.request
from datetime import datetime
from django.shortcuts import render, redirect
from django.utils.http import *

from .vnpay import vnpay


VNPAY_RETURN_URL = 'http://localhost:8000/payment_return'
VNPAY_PAYMENT_URL = 'https://sandbox.vnpayment.vn/paymentv2/vpcpay.html'
VNPAY_API_URL = 'https://sandbox.vnpayment.vn/merchant_webapi/merchant.html'
VNPAY_TMN_CODE = 'I7QZCHYW'
VNPAY_HASH_SECRET_KEY = 'KCDIUJKRNISLAHMXXNTBXALPNHNGGXZZ'


def index(request):
    return render(request, "index.html", {"title": "Danh sách demo"})


def hmacsha512(key, data):
    byteKey = key.encode('utf-8')
    byteData = data.encode('utf-8')
    return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()


def payment(request, order_id, amount):
    ipaddr = get_client_ip(request)
    vnp = vnpay()
    vnp.requestData['vnp_Version'] = '2.1.0'
    vnp.requestData['vnp_Command'] = 'pay'
    vnp.requestData['vnp_TmnCode'] = VNPAY_TMN_CODE
    vnp.requestData['vnp_Amount'] = int(amount) * 100
    vnp.requestData['vnp_CurrCode'] = 'VND'
    vnp.requestData['vnp_TxnRef'] = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(order_id)
    vnp.requestData['vnp_OrderInfo'] = 'Thanh toán đơn hàng ' + str(order_id)
    vnp.requestData['vnp_OrderType'] = 'billpayment'
    vnp.requestData['vnp_Locale'] = 'vn'
    vnp.requestData['vnp_CreateDate'] = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    vnp.requestData['vnp_IpAddr'] = ipaddr
    vnp.requestData['vnp_ReturnUrl'] = VNPAY_RETURN_URL
    vnpay_payment_url = vnp.get_payment_url(VNPAY_PAYMENT_URL, VNPAY_HASH_SECRET_KEY)
    print(vnpay_payment_url)
    return redirect(vnpay_payment_url)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# def query(request):
#     if request.method == 'GET':
#         return render(request, "query.html", {"title": "Kiểm tra kết quả giao dịch"})
#     else:
#         # Add paramter
#         vnp = vnpay()
#         vnp.requestData = {}
#         vnp.requestData['vnp_Command'] = 'querydr'
#         vnp.requestData['vnp_Version'] = '2.1.0'
#         vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
#         vnp.requestData['vnp_TxnRef'] = request.POST['order_id']
#         vnp.requestData['vnp_OrderInfo'] = 'Kiem tra ket qua GD OrderId:' + request.POST['order_id']
#         vnp.requestData['vnp_TransDate'] = request.POST['trans_date']  # 20150410063022
#         vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')  # 20150410063022
#         vnp.requestData['vnp_IpAddr'] = get_client_ip(request)
#         requestUrl = vnp.get_payment_url(settings.VNPAY_API_URL, settings.VNPAY_HASH_SECRET_KEY)
#         responseData = urllib.request.urlopen(requestUrl).read().decode()
#         print('RequestURL:' + requestUrl)
#         print('VNPAY Response:' + responseData)
#         data = responseData.split('&')
#         for x in data:
#             tmp = x.split('=')
#             if len(tmp) == 2:
#                 vnp.responseData[tmp[0]] = urllib.parse.unquote(tmp[1]).replace('+', ' ')

#         print('Validate data from VNPAY:' + str(vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY)))
#         return render(request, "query.html", {"title": "Kiểm tra kết quả giao dịch", "data": vnp.responseData})


# def refund(request):
#     return render(request, "refund.html", {"title": "Gửi yêu cầu hoàn tiền"})