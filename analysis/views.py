from django.shortcuts import render
from EStore.settings import MEDIA_ROOT
from analysis.utils import *
import pandas as pd
import numpy as np
import os


# Create your views here.
def demo_series(request):
    

    return render(request, 'analysis/demo_series.html', {
        
    })


def demo_dataframe(request):
    # Trường hợp 1
    views_likes = np.array([[90006,402], [101141,389], [97297, 403], [117182, 397]])
    df_views_likes_1 = pd.DataFrame(views_likes, columns=['views', 'likes'])
    df_views_likes_html = df_views_likes_1.to_html()

    # Trường hợp 2
    tap_tin = os.path.join(MEDIA_ROOT, 'analysis/data.csv')
    data = pd.read_csv(tap_tin)
    data_html = data.to_html()

    return render(request, 'analysis/demo_dataframe.html', {
        'df_views_likes_html': df_views_likes_html,
        'data_html': data_html,
    })


def work_with_chart(request):
    # Histogram
    data_second = pd.read_excel(os.path.join(MEDIA_ROOT, 'analysis/dataset.xlsx'), sheet_name='Wait_times')
    hist = get_hist(data_second, 'seconds', 'Customer Wait Time')

    # Boxplot
    data_salaries = pd.read_excel(os.path.join(MEDIA_ROOT, 'analysis/salaries.xlsx'))
    box = get_box(data_salaries, 'salary', 'Salary')

    return render(request, 'analysis/chart.html', {
        'hist': hist,
        'box': box,
    })