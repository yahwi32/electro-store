from django.shortcuts import render, HttpResponse
from store.models import Product
from django.db.models import Count
from datetime import datetime
from django.template.loader import render_to_string
from EStore.settings import MEDIA_ROOT
import pdfkit
import os


# Create your views here.
def html_to_pdf(request):
    thoi_gian_hien_tai = datetime.now()

    products = Product.objects.values('subcategory', 'subcategory__name') \
                .annotate(total=Count('subcategory')) \
                .order_by('subcategory')

    response = render_to_string('report.html', {
        'products': products,
        'date': thoi_gian_hien_tai.strftime('%d-%m-%Y'),
    })

    # Xuất PDF
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    pdf_filename = 'report_' + thoi_gian_hien_tai.strftime('%Y%m%d_%H%M%S') + '.pdf'
    pdfkit.from_string(response, os.path.join(MEDIA_ROOT, 'reports', pdf_filename), configuration=config)

    # Tạo link tải báo cáo
    html_string = response + '<div class="text-center"><a href="/media/reports/' + pdf_filename + '" class="btn btn-primary">Tải báo cáo</a></div>'

    return HttpResponse(html_string)