from asyncio.windows_events import NULL
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from tomlkit import date
from web.models import *
from web.vnpay.views import *

class OrderUser:
    def cart(request):
        count_cart = 0
        all_category = Category.objects.filter(category_status=0).order_by()
        all_brand = Brand.objects.filter(brand_status=0).order_by()
        cart = []
        totalprice = totalpayment = 0.0
        ship = 0
        discount = OrderUser.use_voucher(request)
        if 'voucher_code' in request.GET:
            voucher = request.GET['voucher_code']
        if discount == 0:
            voucher = ""
        if "cart" in request.session:
            cart = request.session['cart']
            for item in cart:
                count_cart += item.get('quantity')
                if(item.get('pricesale')>0 and item.get('pricesale')<=item.get('price')):
                    totalprice += item.get('pricesale') * float(item.get('quantity'))
                else:
                    totalprice += item.get('price') * float(item.get('quantity'))
            totalpayment = totalprice + ship - discount
        return render(request, 'home/cart.html', locals())

    def action_cart(request, id=None, quantity=None):
        if id is not None:
            new_cart = []
            if "cart" in request.session:
                cart = request.session['cart']
            for product in cart:
                if int(product['id']) == id:
                    if quantity == 0:
                        product['quantity'] -= 1
                    else:
                        product['quantity'] = int(product['quantity']) + quantity
                    if product['quantity'] <= 0:
                        product['quantity']=1
                    product_obj = Product.objects.get(pk=id)
                    if product['quantity'] > product_obj.pd_quantity:
                        product['quantity'] = product_obj.pd_quantity
                new_cart.append(product)
                request.session['cart'] = new_cart
        if 'add_cart' in request.POST:
            pd_id = request.POST['pd_id']
            if request.POST['quantity']:
                quantity = request.POST['quantity']
            else:
                quantity = 1
            product = Product.objects.get(pk=pd_id)
            cart = []
            if "cart" in request.session:
                cart = request.session['cart']
            new_cart = []
            check = False
            for item in cart:
                id_pd_cart = item.get('id')
                if id_pd_cart == product.pd_id:
                    check = True
                    messages.success(request, "Thêm sản phẩm thành công!")
                    item['quantity'] = int(item['quantity']) + int(quantity)
                    if item['quantity'] > product.pd_quantity:
                        item['quantity'] = product.pd_quantity
                        messages.error(request, "Số lượng của sản phẩm trong giỏ hàng đã bằng số lượng sản phẩm sẵn có!")
                new_cart.append(item)
            if check == False:
                if product.pd_pricesale is None:
                    pricesale = NULL
                else:
                    pricesale = float(product.pd_pricesale)
                new_cart.append({
                    'id': product.pd_id,
                    'name': product.pd_name,
                    'price': float(product.pd_price),
                    'pricesale': pricesale,
                    'image': str(product.pd_img),
                    'quantity': int(quantity)
                })
                messages.success(request, "Thao tác thành công!")
            request.session['cart'] = new_cart
        return redirect(request.META.get('HTTP_REFERER'))

    def cart_delete(request, id=None):
        if id is not None:
            new_cart = []
            if "cart" in request.session:
                cart = request.session['cart']
            for product in cart:
                if product['id'] != id:
                    new_cart.append(product)
            request.session['cart'] = new_cart
        else:
            request.session['cart'] = []
        return redirect(request.META.get('HTTP_REFERER'))

    def checkout(request):
        count_cart = 0
        if 'cart' in request.session:
            cart = request.session['cart']
            for item in cart:
                count_cart += item.get('quantity')
        all_category = Category.objects.filter(category_status=0).order_by()
        all_brand = Brand.objects.filter(brand_status=0).order_by()
        cttk = None
        giohang = []
        if "cart" in request.session:
            giohang = request.session['cart']
        tongtienhang = ship = giamgia = tongthanhtoan = 0.0
        if request.method == 'GET':
            if request.user.is_authenticated:
                id_u = request.user.id
                cttk = UserDetail.objects.get(pk=id_u)
            tongtienhang = request.GET['tongtienhang']
            ship = request.GET['ship']
            giamgia = request.GET['giamgia']
            if giamgia == '0':
                magiamgia = ""
            else:
                magiamgia = request.GET['magiamgia']
            tongthanhtoan = request.GET['tongthanhtoan']
            return render(request, 'home/checkout.html', locals())
        elif request.method == 'POST':
            if request.user.is_authenticated:
                id_u = request.user.id
                cttk = UserDetail.objects.get(pk=id_u)
            hoten = request.POST['hoten']
            sdt = request.POST['sdt']
            diachi = request.POST['diachi']
            email = request.POST['email']
            tongtienhang = request.POST['tongtienhang']
            ship = request.POST['ship']
            giamgia = request.POST['giamgia']
            if giamgia == '0':
                magiamgia = None
            else:
                magiamgia = request.POST['magiamgia']
            tongthanhtoan = request.POST['tongthanhtoan']
            dh = Order(order_name=hoten, order_phone=sdt, order_address=diachi, order_email=email, order_totalprice=tongthanhtoan,
                        order_ship=ship,order_voucher_code=magiamgia, order_discount=giamgia, order_payment=0, order_status = 0)
            dh.save()
            try:
                voucher_used = Voucher.objects.get(voucher_code=magiamgia)
                voucher_used.voucher_quantity -= 1
                if voucher_used.voucher_quantity < 1:
                    voucher_used.voucher_quantity = 0
                voucher_used.save()
            except:
                pass
            id_dh = dh.order_id
            payment_method = request.POST['payment_method']
            if request.user.is_authenticated:
                user = User.objects.get(pk=id_u)
                tk_dh = Order.objects.get(pk=id_dh)
                tk_dh.user = user
                tk_dh.save()
            for item in giohang:
                sp = Product.objects.get(pk=item.get('id'))
                dh = Order.objects.get(pk=id_dh)
                OrderDetail(od_nameproduct=item.get('name'), od_quantity=item.get('quantity'), od_price=item.get('price'),od_pricesale=item.get('pricesale'), product=sp, order=dh).save()
                sp.pd_quantity -= item.get('quantity')
                if sp.pd_quantity < 1:
                    sp.pd_quantity = 0
                sp.save()
            del request.session['cart']
            if payment_method == '1':
                tongthanhtoan = int(float(tongthanhtoan))
                return payment(request, id_dh, tongthanhtoan)
            else:
                return redirect ('order_detail', id=id_dh)
        else:
            return redirect(request.META.get('HTTP_REFERER'))
    
    def payment_return(request):
        inputData = request.GET
        if inputData:
            vnp = vnpay()
            vnp.responseData = inputData.dict()
            order_id = inputData['vnp_TxnRef']
            amount = int(inputData['vnp_Amount']) / 100
            order_desc = inputData['vnp_OrderInfo']
            vnp_TransactionNo = inputData['vnp_TransactionNo']
            vnp_ResponseCode = inputData['vnp_ResponseCode']
            vnp_TmnCode = inputData['vnp_TmnCode']
            vnp_PayDate = inputData['vnp_PayDate']
            vnp_BankCode = inputData['vnp_BankCode']
            vnp_CardType = inputData['vnp_CardType']
            if vnp.validate_response(VNPAY_HASH_SECRET_KEY):
                if vnp_ResponseCode == "00":
                    order_id = order_id[14:]
                    order = Order.objects.get(pk=order_id)
                    order.order_status = 1
                    order.order_code_payment = vnp_TransactionNo
                    order.save()
                else:
                    messages.error(request, "Thanh toán qua VNPAY không thành công vui lòng liên hệ cửa hàng để được hỗ trợ tốt nhất! Cảm ơn quý khách rất nhiều!")
            else:
                messages.error(request, "Thanh toán qua VNPAY không thành công vui lòng liên hệ cửa hàng để được hỗ trợ tốt nhất! Cảm ơn quý khách rất nhiều!")
        else:
            messages.error(request, "Thanh toán qua VNPAY không thành công vui lòng liên hệ cửa hàng để được hỗ trợ tốt nhất! Cảm ơn quý khách rất nhiều!")
        return redirect ('order_detail', id=order_id)

    def order_detail(request, id=None):
        all_category = Category.objects.filter(category_status=0).order_by()
        all_brand = Brand.objects.filter(brand_status=0).order_by()
        count_cart = 0
        if 'cart' in request.session:
            cart = request.session['cart']
            for item in cart:
                count_cart += item.get('quantity')
        dh = Order.objects.get(pk=id)
        ctdh = OrderDetail.objects.filter(order=id)
        return render(request, 'home/order_detail.html', locals())

    def use_voucher(request):
        discount = 0.0
        now = datetime.datetime.now()
        if 'voucher_code' in request.GET:
            totalprice = 0.0
            if "cart" in request.session:
                cart = request.session['cart']
                for item in cart:
                    if(item.get('pricesale')>0 and item.get('pricesale')<=item.get('price')):
                        totalprice += item.get('pricesale') * float(item.get('quantity'))
                    else:
                        totalprice += item.get('price') * float(item.get('quantity'))
            voucher_code = request.GET['voucher_code']
            try:
                voucher = Voucher.objects.get(voucher_code=voucher_code)
                if voucher.voucher_active == '1':
                    if voucher.voucher_quantity is None:
                        if voucher.voucher_value < 1:
                            discount = totalprice * voucher.voucher_value
                            # messages.error(request, "Thêm sản phẩm thành công!")
                        else:
                            discount = totalprice - (totalprice - voucher.voucher_value)
                        # if voucher.voucher_date_start is None and voucher.voucher_date_end is None:
                        #     if voucher.voucher_value < 1:
                        #         discount = totalprice * voucher.voucher_value
                        #         # messages.error(request, "Thêm sản phẩm thành công!")
                        #     else:
                        #         discount = totalprice - voucher.voucher_value
                        # elif voucher.voucher_date_start is None and voucher.voucher_date_end:
                        #     if now < voucher.voucher_date_end:
                        #         if voucher.voucher_value < 1:
                        #             discount = totalprice * voucher.voucher_value
                        #         else:
                        #             discount = totalprice - voucher.voucher_value
                        # elif voucher.voucher_date_end is None and voucher.voucher_date_start:
                        #     if now > voucher.voucher_date_start:
                        #         if voucher.voucher_value < 1:
                        #             discount = totalprice * voucher.voucher_value
                        #         else:
                        #             discount = totalprice - voucher.voucher_value
                        # else:
                        #     if now > voucher.voucher_date_start and now < voucher.voucher_date_start:
                        #         if voucher.voucher_value < 1:
                        #             discount = totalprice * voucher.voucher_value
                        #         else:
                        #             discount = totalprice - voucher.voucher_value
                    elif voucher.voucher_quantity > 0:
                        if voucher.voucher_value < 1:
                            discount = totalprice * voucher.voucher_value
                            # messages.error(request, "Thêm sản phẩm thành công!")
                        else:
                            discount = totalprice - (totalprice - voucher.voucher_value)
                    else:
                        messages.error(request, "Mã giảm giá hết lượt!")
                else:
                    discount = 0
            except:
                discount = 0
                messages.error(request, "Mã giảm giá không tồn tại!")
        return discount