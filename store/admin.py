from django.contrib import admin
from store.models import Product
from customer.models import Customer
from datetime import datetime
from django.utils.html import format_html
from cart.models import Order,OrderItem

# Register your models here
def change_public_day(modeladmin, request, queryset):
    queryset.update(public_day=datetime.now())


change_public_day.short_description = 'Thay doi public_day sang ngay hien tai'


class ProductAdmin(admin.ModelAdmin):
    # Loại bỏ các fields không cần thiết hiển thị (insert/update)
    exclude = ('public_day', 'viewed')
    
    # Hiển thị các fields chỉ định
    # list_display = ('name', 'price', 'price_origin', 'public_day', 'viewed')
    list_display = ('e_name', 'e_price', 'e_price_origin', 'e_public_day', 'e_viewed', 'e_image')

    # Filter theo các fields chỉ định
    list_filter = ('public_day',)

    # Tìm kiếm
    search_fields = ('name__contains',)

    # Action
    actions = [change_public_day]


    # Tham khảo: https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display
    @admin.display(description='Tên sản phẩm')
    def e_name(self, obj):
        return ("%s" % obj.name.upper())

    @admin.display(description='Giá bán')
    def e_price(self, obj):
        return ("%s" % '{:,}'.format(int(obj.price)))

    @admin.display(description='Giá gốc')
    def e_price_origin(self, obj):
        return ("%s" % '{:,}'.format(int(obj.price_origin)))

    @admin.display(description='Ngày đăng')
    def e_public_day(self, obj):
        return ("%s" % obj.public_day)

    @admin.display(description='Số lượt xem')
    def e_viewed(self, obj):
        return ("%s" % obj.viewed)

    @admin.display(description='Hình ảnh')
    def e_image(self, obj):
        return format_html('<img src="{}" alt="{}" width="45px" height="45px" />'.format(obj.image.url, obj.name))

admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Customer)
# Thay đổi tiêu đề
admin.site.site_header = 'EStore Administration'