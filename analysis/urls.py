from django.urls import path
from analysis.views import *


app_name = 'analysis'
urlpatterns = [
    path('demo-series/', demo_series, name='demo_series'),
    path('demo-dataframe/', demo_dataframe, name='demo_dataframe'),
    path('chart/', work_with_chart, name='work_with_chart'),
]
