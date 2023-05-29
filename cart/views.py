from itertools import product
from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from store.models import Product
from cart.models import Order, OrderItem
from customer.models import Customer
from django.views.decorators.http import require_POST


# Create your views here.
def cart_detail(request):
    cart = Cart(request)

    # Mã giảm giá (coupon)
    list_ma_giam_gia = [
        {
            'TTTH': 0.8,
        },
        {
            'LNTRI': 0.9,
        },
    ]

    ma_giam_gia = ''
    giam_gia = 1
    if request.POST.get('btnMaGiamGia'):
        ma_giam_gia = request.POST.get('ma_giam_gia')  # TTTH
        for dict_ma_giam_gia in list_ma_giam_gia:
            if ma_giam_gia in dict_ma_giam_gia:
                cart_new = {}
                giam_gia = dict_ma_giam_gia[ma_giam_gia]
                for c in cart:
                    product_cart = {
                        str(c['product'].pk): {
                            'quantity': c['quantity'], 
                            'price': str(c['product'].price), 
                            'coupon': str(giam_gia)
                        }
                    }
                    cart_new.update(product_cart)

                    # Giữ lại số lượng mới trên ô tại thời điểm click nút
                    c['coupon'] = giam_gia
                else:
                    # Cập nhật session giỏ hàng (cart)
                    request.session['cart'] = cart_new
                break
        else:
            cart_new = {}
            for c in cart:
                product_cart = {
                    str(c['product'].pk): {
                        'quantity': c['quantity'], 
                        'price': str(c['product'].price), 
                        'coupon': str(giam_gia)
                    }
                }
                cart_new.update(product_cart)

                # Giữ lại số lượng mới trên ô tại thời điểm click nút
                c['coupon'] = giam_gia
            else:
                # Cập nhật session giỏ hàng (cart)
                request.session['cart'] = cart_new

    # Cập nhật giỏ hàng
    if request.POST.get('btnCapNhat'):
        cart_new = {}
        for c in cart:
            quantity_new = int(request.POST.get('quantity2' + str(c['product'].pk)))
            if quantity_new != 0:
                product_cart = {
                    str(c['product'].pk): {
                        'quantity': quantity_new, 
                        'price': str(c['product'].price), 
                        'coupon': str(c['coupon'])
                    }
                }
                cart_new.update(product_cart)
            else:
                # Xóa sản phẩm ra khỏi giỏ hàng khi số lượng mới = 0
                cart.remove(c['product'])

            # Giữ lại số lượng mới trên ô tại thời điểm click nút
            c['quantity'] = quantity_new
        else:
            # Cập nhật session giỏ hàng (cart)
            request.session['cart'] = cart_new

    return render(request, 'store/cart.html', {
        'cart': cart,
        'ma_giam_gia': ma_giam_gia,
    })


def checkout(request):
    # Kiểm tra trạng thái đăng nhập của khách hàng
    if 'session_KhachHang' not in request.session:
        return redirect('cart:cart_detail')

    # Đọc thông tin giỏ hàng từ session cart
    cart = Cart(request)

    # Thực hiện đặt hàng
    if request.POST.get('btnDatHang'):
        # Lấy thông tin khách hàng (người đặt hàng)
        customer = Customer.objects.get(pk=request.session.get('session_KhachHang')['id'])

        # Order
        order = Order()
        order.total = cart.get_final_total_price()
        order.customer = customer
        order.save()

        # OrderItem
        for c in cart:
            OrderItem.objects.create(order=order,
                                     product=c['product'],
                                     price=c['price'],
                                     quantity=c['quantity'])

        # Gửi mail

        # Xóa session cart khi đặt hàng thành công
        cart.clear()

        return render(request, 'cart/result.html', {
            'cart': cart,
        })

    return render(request, 'store/checkout.html', {
        'cart': cart,
    })


@require_POST
def buy_now(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if request.POST.get('quantity'):
        cart.add(product, int(request.POST.get('quantity')))
    return redirect('cart:cart_detail')


@require_POST
def remove_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')
