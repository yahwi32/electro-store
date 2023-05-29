from django.shortcuts import render, redirect
from customer.forms import FormSignUp, FormSignUp2
from customer.models import Customer
from django.contrib.auth.hashers import PBKDF2PasswordHasher, Argon2PasswordHasher, BCryptPasswordHasher, CryptPasswordHasher
from customer.libs import *
from cart.models import Order, OrderItem
from store.models import Product


# Create your views here.
def customer_login_2(request):
    # Kiểm tra trạng thái của session
    if 'session_KhachHang' in request.session:
        return redirect('store:index')

    # Lấy thông tin tỉnh/tp, quận/huyện, phường/xã
    du_lieu = read_json_internet('http://api.laptrinhpython.net/vietnam')
    
    # Tỉnh/TP
    list_provinces = []
    str_districts = []
    str_wards = []
    list_districts_2 = []
    for province in du_lieu:
        list_provinces.append(province['name'])

        # Quận/Huyện
        list_districts = []
        for dictrict in province['districts']:
            d = dictrict['prefix'] + ' ' + dictrict['name']
            list_districts.append(d)
            list_districts_2.append(d)

            # Phường/Xã
            list_wards = []
            for ward in dictrict['wards']:
                w = ward['prefix'] + ' ' + ward['name']
                list_wards.append(w)
            else:
                str_wards.append('|'.join(list_wards))

        else:
            str_districts.append('|'.join(list_districts))

    # Đăng ký
    result_signup = ''
    form_signup = FormSignUp2()
    if request.POST.get('btnDangKy'):
        form_signup = FormSignUp2(request.POST, Customer)
        if form_signup.is_valid() and form_signup.cleaned_data['password'] == form_signup.cleaned_data['confirm_password']:
            # Lưu vào CSDL
            hasher = Argon2PasswordHasher()
            request.POST._mutable = True
            post = form_signup.save(commit=False)
            post.last_name = form_signup.cleaned_data['last_name']
            post.first_name = form_signup.cleaned_data['first_name']
            post.email = form_signup.cleaned_data['email']
            post.tel = form_signup.cleaned_data['tel']
            post.password = hasher.encode(form_signup.cleaned_data['password'], '12345678')  # salt
            post.address = form_signup.cleaned_data['address'] + ', ' + form_signup.cleaned_data['phuong_xa'] \
                            + ', ' + form_signup.cleaned_data['quan_huyen'] + ', ' + form_signup.cleaned_data['tinh_tp']
            post.save()

            # Gửi mail

            result_signup = '''
            <div class="alert alert-success" role="alert">
                Đăng ký thành viên thành công.
            </div>
            '''
        else:
            result_signup = '''
            <div class="alert alert-danger" role="alert">
                Đăng ký thành viên không thành công. Vui lòng kiểm tra lại thông tin nhập.
            </div>
            '''

    # Đăng nhập
    if request.POST.get('btnDangNhap'):
        # Gán biến
        email = request.POST.get('email')
        mat_khau = request.POST.get('mat_khau')
        hasher = Argon2PasswordHasher()
        encoded = hasher.encode(mat_khau, '12345678')

        khach_hang = Customer.objects.filter(email=email, password=encoded)
        if khach_hang.count() > 0:
            # print(khach_hang.values())
            # <QuerySet [{'id': 1, 'first_name': 'Lê Ngọc', 'last_name': 'Trí', 'email': 'lntri@csc.hcmus.edu.vn', 'password': '123', 'tel': '0902377795', 'address': 'TPHCM'}]>
            # print(khach_hang.values()[0])
            # {'id': 1, 'first_name': 'Lê Ngọc', 'last_name': 'Trí', 'email': 'lntri@csc.hcmus.edu.vn', 'password': '123', 'tel': '0902377795', 'address': 'TPHCM'}
            
            request.session['session_KhachHang'] = khach_hang.values()[0]
            return redirect('store:index')

    return render(request, 'store/login-2.html', {
        'form_signup': form_signup,
        'result_signup': result_signup,
        'provinces': tuple(list_provinces),
        'str_districts': tuple(str_districts),
        'str_wards': tuple(str_wards),
        'list_districts': list_districts_2,
    })


def customer_login(request):
    # Kiểm tra trạng thái của session
    if 'session_KhachHang' in request.session:
        return redirect('store:index')

    # Đăng ký
    result_signup = ''
    form_signup = FormSignUp()
    if request.POST.get('btnDangKy'):
        form_signup = FormSignUp(request.POST, Customer)
        if form_signup.is_valid() and form_signup.cleaned_data['password'] == form_signup.cleaned_data['confirm_password']:
            # Lưu vào CSDL
            hasher = Argon2PasswordHasher()
            request.POST._mutable = True
            post = form_signup.save(commit=False)
            post.last_name = form_signup.cleaned_data['last_name']
            post.first_name = form_signup.cleaned_data['first_name']
            post.email = form_signup.cleaned_data['email']
            post.tel = form_signup.cleaned_data['tel']
            post.password = hasher.encode(form_signup.cleaned_data['password'], '12345678')  # salt
            post.address = form_signup.cleaned_data['address']
            post.save()

            # Gửi mail
            subject = 'Đăng ký tài khoản mới ' + post.email
            content = 'Chào mừng ...'
            '''
            EMAIL_HOST_USER
            [1, 2, 3]
            '''

            result_signup = '''
            <div class="alert alert-success" role="alert">
                Đăng ký thành viên thành công.
            </div>
            '''
        else:
            result_signup = '''
            <div class="alert alert-danger" role="alert">
                Đăng ký thành viên không thành công. Vui lòng kiểm tra lại thông tin nhập.
            </div>
            '''

    # Đăng nhập
    if request.POST.get('btnDangNhap'):
        # Gán biến
        email = request.POST.get('email')
        mat_khau = request.POST.get('mat_khau')
        hasher = Argon2PasswordHasher()
        encoded = hasher.encode(mat_khau, '12345678')

        khach_hang = Customer.objects.filter(email=email, password=encoded)
        if khach_hang.count() > 0:
            # print(khach_hang.values())
            # <QuerySet [{'id': 1, 'first_name': 'Lê Ngọc', 'last_name': 'Trí', 'email': 'lntri@csc.hcmus.edu.vn', 'password': '123', 'tel': '0902377795', 'address': 'TPHCM'}]>
            # print(khach_hang.values()[0])
            # {'id': 1, 'first_name': 'Lê Ngọc', 'last_name': 'Trí', 'email': 'lntri@csc.hcmus.edu.vn', 'password': '123', 'tel': '0902377795', 'address': 'TPHCM'}
            
            request.session['session_KhachHang'] = khach_hang.values()[0]
            return redirect('store:index')

    return render(request, 'store/login.html', {
        'form_signup': form_signup,
        'result_signup': result_signup,
    })


def customer_logout(request):
    if 'session_KhachHang' in request.session:
        del request.session['session_KhachHang']
    return redirect('customer:customer_login')


def my_account(request):
    if 'session_KhachHang' not in request.session:
        return redirect('store:index')

    # Cập nhật thông tin khách hàng
    result_update_info = ''
    if request.POST.get('btnCapNhat'):
        # Gán biến
        ho = request.POST.get('ho')
        ten = request.POST.get('ten')
        dien_thoai = request.POST.get('dien_thoai')
        # email = request.POST.get('email')
        dia_chi = request.POST.get('dia_chi')

        # Cập nhật vào CSDL
        khach_hang = Customer.objects.get(id=request.session['session_KhachHang']['id'])
        khach_hang.first_name = ten
        khach_hang.last_name = ho
        khach_hang.tel = dien_thoai
        khach_hang.address = dia_chi
        khach_hang.save()

        # Cập nhật vào session
        request.session['session_KhachHang']['first_name'] = ten
        request.session['session_KhachHang']['last_name'] = ho
        request.session['session_KhachHang']['tel'] = dien_thoai
        request.session['session_KhachHang']['address'] = dia_chi

        # Thông báo kết quả
        result_update_info = '''
        <div class="alert alert-success" role="alert">
            Cập nhật thông tin thành công.
        </div>
        '''

    # Đổi mật khẩu

    # Đơn hàng
    orders = Order.objects.filter(customer=request.session['session_KhachHang']['id'])
    dict_orders = {}
    for order in orders:
        order_items = list(OrderItem.objects.filter(order=order.pk).values())
        for order_item in order_items:
            product = Product.objects.get(pk=order_item['product_id'])
            order_item['product_name'] = product.name
            order_item['product_image'] = product.image
            order_item['total_price'] = order.total
        else:
            dict_order_items = {
                order.pk: order_items
            }
            dict_orders.update(dict_order_items)

    return render(request, 'store/my-account.html', {
        'result_update_info': result_update_info,
        'orders': orders,
        'dict_orders': dict_orders,
    })