"""
    coding      : UTF-8
    Environment : Python 3.6
    Author      : Benjamin142857
    Data        : 10/14/2019
    Remark      : urls
"""
from django.conf.urls import url
from crm import views

app_name = 'crm'

urlpatterns = [
    # 出版社Press
    url(r'^page_list/', views.page_list),
    url(r'^page_list2/', views.page_list2),
]