from django.urls import path
from store_report.views import *


app_name = 'store_report'
urlpatterns = [
    path('report/', html_to_pdf)
]
