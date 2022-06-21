# Page for user
from web.homefile.home import *
from web.homefile.account import *
from web.homefile.order import *
from web.homefile.product import *

# Page for admin
from web.adminfile.home import *
from web.adminfile.category import *
from web.adminfile.brand import *
from web.adminfile.product import *
from web.adminfile.voucher import *
from web.adminfile.chat import *
from web.adminfile.order import *

# VNPay
from web.vnpay.views import *


# @register.simple_tag
# def check_price_product(discount, active, start, end):
#     now = datetime.now()
#     result = True
#     if discount and active:
#         if not start and not end:
#             result = True
#         elif not start and end:
#             if now < end:
#                 result = True
#             else:
#                 result = False
#         elif not end and start:
#             if now > start:
#                 result = True
#             else:
#                 result = False
#         elif now > start and now < end:
#             result = True
#         else:
#             result = False
#     else:
#         result = False
#     return result