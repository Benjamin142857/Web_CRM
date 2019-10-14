"""
    coding      : UTF-8
    Environment : Python 3.6
    Author      : Benjamin142857
    Data        : 10/6/2019
    Remark      : other
"""


def get_page_range(total_page, now_page, max_page_show):
    if total_page <= max_page_show:
        ret = (range(1, total_page+1), 0)
    else:
        h_show = max_page_show // 2
        if now_page <= 1 + h_show:
            ret = (range(1, max_page_show+1), 1)
        elif now_page >= total_page - h_show:
            ret = (range(total_page-max_page_show+1, total_page+1), 3)
        else:
            ret = (range(now_page-h_show, now_page+h_show+1), 2)
    return ret


if __name__ == '__main__':
    a, b = get_page_range(15, 144, 9)
    print(list(a))
    print(b)
