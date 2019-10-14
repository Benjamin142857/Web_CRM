"""
    coding      : UTF-8
    Environment : Python 3.6
    Author      : Benjamin142857
    Data        : 10/6/2019
    Remark      : form
"""
from django import forms

page_str = request.GET.get('page')
num = int(page_str) if page_str and re.findall(r'^\d+$', page_str) else 1

if __name__ == '__main__':
    pass
