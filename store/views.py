from django.shortcuts import render, reverse, redirect
from store.models import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from rest_framework import viewsets, permissions
from store.serializers import ProductSerializer
from urllib.parse import urlencode
from EStore.settings import MEDIA_ROOT
import pandas as pd
import re
import os
from store.forms import FormContact
# Create your views here
def index(request):
    # Laptop
    subcategory_id_laptop = SubCategory.objects.filter(category_id=1).values_list('id')
    list_subcategory_id_laptop = []
    for subcategory_id in subcategory_id_laptop:
        list_subcategory_id_laptop.append(subcategory_id[0])
    # Lấy danh sách sản phẩm
    products_laptop = Product.objects.filter(subcategory__in=list_subcategory_id_laptop).order_by('-public_day')

     # CPU
    subcategory_id_cpu = SubCategory.objects.filter(category_id=2).values_list('id')
    print(subcategory_id_cpu)
    list_subcategory_id_cpu = []
    for subcategory_id in subcategory_id_cpu:
        list_subcategory_id_cpu.append(subcategory_id[0])
    # Lấy danh sách sản phẩm
    products_cpu = Product.objects.filter(subcategory__in=list_subcategory_id_cpu).order_by('-public_day')


    # top selling laptop
    subcategory_id_selling_latop = SubCategory.objects.filter(category_id=1).values_list('id')
    list_subcategory_id_selling_latop = []
    for subcategory_id in subcategory_id_selling_latop:
        list_subcategory_id_selling_latop.append(subcategory_id[0])
    # Lấy danh sách sản phẩm
    products_selling_latop = Product.objects.filter(subcategory__in=list_subcategory_id_selling_latop).order_by('-viewed')

     # top selling linkkien
    subcategory_id_selling_linh_kien = SubCategory.objects.filter(category_id=2).values_list('id')
    list_subcategory_id_selling_linh_kien = []
    for subcategory_id in subcategory_id_selling_linh_kien:
        list_subcategory_id_selling_linh_kien.append(subcategory_id[0])
    # Lấy danh sách sản phẩm
    products_selling_linh_kien = Product.objects.filter(subcategory__in=list_subcategory_id_selling_linh_kien).order_by('-viewed')

     # top selling gameinggear
    subcategory_id_selling_gear = SubCategory.objects.filter(category_id=3).values_list('id')
    list_subcategory_id_selling_gear = []
    for subcategory_id in subcategory_id_selling_gear:
        list_subcategory_id_selling_gear.append(subcategory_id[0])
    # Lấy danh sách sản phẩm
    products_selling_gear = Product.objects.filter(subcategory__in=list_subcategory_id_selling_gear).order_by('-viewed')
    
    return render(request, 'store/index.html', {
    'products_laptop':products_laptop,
    'products_cpu':products_cpu,
    'products_selling_latop':products_selling_latop,
    'products_selling_linh_kien':products_selling_linh_kien,
    'products_selling_gear':products_selling_gear,
    })
def subcategory(request, pk):
     # Danh sách subcategory
    subcategories = SubCategory.objects.order_by('name')

    if pk == 0:
        # Đọc tất cả sp
        products = Product.objects.order_by('-public_day')
        title_subcategory = 'Tất cả sản phẩm (' + str(products.count()) + ')'
    else:
        # Đọc sản phẩm theo subcategory_id
        products = Product.objects.filter(subcategory=pk).order_by('-public_day')
        name_subcategory = SubCategory.objects.get(pk=pk)
        title_subcategory = str(name_subcategory) + ' (' + str(products.count()) + ')'

    # Lọc theo range giá
    tu_gia = ''
    den_gia = ''
    tu_khoa = ''
    if request.GET.get('from_price'):
        tu_gia = float(request.GET.get('from_price'))
        den_gia = float(request.GET.get('to_price'))
        tu_khoa = request.GET.get('product_name')

        # Nếu có chứa từ khóa tìm kiếm (product_name) 
        if tu_khoa != '':
            products = Product.objects.filter(name__contains=tu_khoa).order_by('-public_day')

        products = [product for product in products if tu_gia <= product.price <= den_gia]  # list comprehension
        title_subcategory = 'Tìm thấy {} sản phẩm trong khoảng giá {} - {}'.format(len(products), '{:,}'.format(int(tu_gia)), '{:,}'.format(int(den_gia)))

    # Phân trang
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 15)
    products_pager = paginator.page(page)
    return render(request,'store/product-list.html',{
        'subcategories': subcategories,
        'products': products_pager,
        'title_subcategory': title_subcategory,
        'tu_gia': tu_gia,
        'den_gia': den_gia,
    })

def search_products(request):
    tu_khoa = ''
    if request.GET.get('product_name'):
        tu_khoa = request.GET.get('product_name').strip()

        products = Product.objects.filter(name__contains=tu_khoa).order_by('-public_day')
        title_subcategory = 'Tìm thấy {} sản phẩm với từ khóa "{}"'.format(products.count(), tu_khoa)

    # Phân trang
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 15)
    products_pager = paginator.page(page)

    tu_gia = ''
    den_gia = ''
    if request.GET.get('from_price'):
        tu_gia = float(request.GET.get('from_price'))
        den_gia = float(request.GET.get('to_price'))
        tu_khoa = request.GET.get('product_name')

        base_url = reverse('store:subcategory', kwargs={'pk': 0})
        query_string = urlencode({
            'from_price': round(tu_gia),
            'to_price': round(den_gia),
            'product_name': tu_khoa
        })
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)


    return render(request, 'store/product-list.html', {
        'tu_khoa': tu_khoa,
        'title_subcategory': title_subcategory,
        'products': products_pager,
    })
#Web Service 
def products_service(request):
    products = Product.objects.all()
    result_list = list(products.values('name', 'price', 'public_day'))
    return JsonResponse(result_list, safe=False)


# Django Rest Framework
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


def product_detail(request, pk):
    # Danh sách subcategory
    subcategories = SubCategory.objects.order_by('name')

    # Lấy sản phẩm
    product = Product.objects.get(pk=pk)

    # Sản phẩm liên quan
    id_subcategory = product.subcategory.pk
    products_related = Product.objects.filter(subcategory=id_subcategory).exclude(pk=pk).order_by('-public_day')[:20]

    # Tên danh mục
    subcategory_name = product.subcategory

    #sản phẩm nhiều lượt xem
    view_product=Product.objects.order_by('-viewed')[:20]
    # Hiển thị sản phẩm thường được mua kèm
    rules = pd.read_csv(os.path.join(MEDIA_ROOT, 'rules.csv'), squeeze=True, index_col=0)
    lst = rules.values.tolist()
    list_rules = []
    for item in lst:
        if str(pk) in re.findall('\d+[, \d+]*', item[0])[0].split(','):
            list_rules = re.findall('\d+[, \d+]*', item[1])[0].split(',')
    list_asc_products = []
    for i in list_rules:
        list_asc_products.append(Product.objects.get(pk=int(i)))

    return render(request, 'store/product-detail.html', {
        'subcategories': subcategories,
        'product': product,
        'products_related': products_related,
        'subcategory_name': subcategory_name,
        'id_subcategory': id_subcategory,
        'list_asc_products': list_asc_products,
        'view_product':view_product,
    })

def contact(request):
    form = FormContact()
    result = ''
    if request.POST.get('btnSend'):  # sự kiện click nút
        form = FormContact(request.POST, Contact)
        if form.is_valid():
            request.POST._mutable = True
            post = form.save(commit=False)
            post.name = form.cleaned_data['name']
            post.email = form.cleaned_data['email']
            post.subject = form.cleaned_data['subject']
            post.message = form.cleaned_data['message']
            post.save()

            result = '''
            <div class="alert alert-success" role="alert">
                Gửi thông tin thành công.
            </div>
            '''
            
    return render(request, 'store/contact.html', {
        'form': form,
        'result': result,
    })