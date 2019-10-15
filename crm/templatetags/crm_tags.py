"""
    coding      : UTF-8
    Environment : Python 3.6
    Author      : Benjamin142857
    Data        : 10/14/2019
    Remark      : crm_tags
"""

from django import template

register = template.Library()


@register.inclusion_tag(filename='inclusion_tag/pagination.html')
def pagination(pagination):
    url = pagination['url']                                     # 页数对应url
    max_page = pagination['max_page']                           # 总页数
    now_page = pagination['now_page']                           # 当前页数
    pagination_max_show = pagination['pagination_max_show']     # pagination 最大显示页 (奇数)

    # 1. 生成当前 pagination 展示页码列表
    if max_page <= pagination_max_show:
        page_lst = list(range(1, max_page+1))
    else:
        h_show = pagination_max_show // 2

        # 1.1 当前页数过于靠前，取前 pagiation_max_show
        if now_page <= 1 + h_show:
            page_lst = list(range(1, pagination_max_show + 1))
        # 1.2 当前页数过于靠后，取后 pagiation_max_show
        elif now_page >= max_page - h_show:
            page_lst = list(range(max_page - pagination_max_show + 1, max_page + 1))
        # 1.3 当前页数居中展示
        else:
            page_lst = list(range(now_page-h_show, now_page+h_show+1))

    return {'url': url, 'page_lst': page_lst, 'now_page': now_page, 'max_page': max_page}

