from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from crm import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^crm/', include('crm.urls', namespace='CRM')),
    url(r'^benjamin/', views.page_list, name='benjamin'),
    url(r'^stella/', views.page_list, name='stella'),
]
