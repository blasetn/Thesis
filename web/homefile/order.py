from asyncio.windows_events import NULL
from django.shortcuts import render, redirect
from django.contrib import messages
from web.models import *
from web.vnpay.views import *

class OrderUser:
    def cart(request):
        cart = []
        totalprice = totalpayment = 0.0
        ship = 0
        discount = 0
        if "cart" in request.session:
            cart = request.session['cart']
            for item in cart:
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
            tongthanhtoan = request.POST['tongthanhtoan']
            dh = Order(order_name=hoten, order_phone=sdt, order_address=diachi, order_email=email, order_totalprice=tongthanhtoan,
                        order_ship=ship, order_discount=giamgia, order_payment=0, order_status = 0)
            dh.save()
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
                sp.save()
            # del request.session['cart']
            tongthanhtoan = int(float(tongthanhtoan))/10000
            return payment(request, id_dh, tongthanhtoan)
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
                    order.save()
                    return redirect ('order_detail', id=order_id)


    def order_detail(request, id=None):
        dh = Order.objects.get(pk=id)
        ctdh = OrderDetail.objects.filter(order=id)
        return render(request, 'home/order_detail.html', locals())