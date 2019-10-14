import re
import math

from django.shortcuts import render
from utils.other import get_page_range


def page_list(request):
    page_str = request.GET.get('page')
    page_num = int(page_str) if page_str and re.findall(r'^\d+$', page_str) else 1
    ret_lst = [{'name': 'benjamin_{}'.format(i), 'age': i} for i in range(300)]
    ret_lst_length = len(ret_lst)
    one_page_max_show = 20

    page_lst, show_cls = get_page_range(total_page=math.ceil(ret_lst_length/one_page_max_show), now_page=page_num, max_page_show=8)
    now_page_lst = ret_lst[(page_num-1)*one_page_max_show: page_num*one_page_max_show]
    print(show_cls)
    return render(request, 'crm/page_list.html', {'now_page_list': now_page_lst, 'page_list': page_lst})
