import re
import math

from django.shortcuts import render, HttpResponse, redirect
from django.views import View


def page_list(request):
    # print('\n\n\n')
    # for k, v in request.META.items():
    #     print('"{}": "{}"'.format(k, v))
    # print(request.path)
    # print(request.path_info)

    now_page_str = request.GET.get('page')
    now_page = int(now_page_str) if now_page_str and re.findall(r'^\d+$', now_page_str) else 1
    one_page_max_show = 20
    all_data = [{'name': 'benjamin_{}'.format(i), 'age': i} for i in range(300)]
    max_page = math.ceil(len(all_data)/one_page_max_show)
    if now_page < 1 or now_page > max_page:
        ret_data = all_data[0:one_page_max_show]
        now_page = 1
    else:
        ret_data = all_data[(now_page-1)*one_page_max_show: now_page*one_page_max_show]

    pagination = {
        'url': '/crm/page_list/',
        'now_page': now_page,
        'max_page': max_page,
        'pagination_max_show': 9,
    }
    print('abc')
    return render(request, 'crm/page_list.html', {'data': ret_data, 'pagination': pagination})


def page_list2(request):
    now_page_str = request.GET.get('page')
    now_page = int(now_page_str) if now_page_str and re.findall(r'^\d+$', now_page_str) else 1
    one_page_max_show = 20
    all_data = [{'name': 'stella_{}'.format(i), 'age': i} for i in range(900)]
    max_page = math.ceil(len(all_data) / one_page_max_show)
    if now_page<1 or now_page>max_page:
        ret_data = all_data[0:one_page_max_show]
        now_page = 1
    else:
        ret_data = all_data[(now_page - 1) * one_page_max_show: now_page * one_page_max_show]

    pagination = {
        'url': '/crm/page_list2/',
        'now_page': now_page,
        'max_page': max_page,
        'pagination_max_show': 11,
    }
    return render(request, 'crm/page_list2.html', {'data': ret_data, 'pagination': pagination})


def test(request):
    qd = request.GET
    qd._mutable = True
    qd['next'] = '/crm/test/?a=2&b=3'
    print(qd)
    for k, v in qd.items():
        print(k, type(v))
    return redirect('/crm/page_list/{}'.format(qd.urlencode()))