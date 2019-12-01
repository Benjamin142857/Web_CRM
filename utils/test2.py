"""
    coding      : UTF-8
    Environment : Python 3.6
    Author      : Benjamin142857
    Data        : 11/26/2019
    Remark      : test2
"""
import importlib
from Web_CRM import settings
from Web_CRM.urls import urlpatterns
from django.urls import URLResolver, URLPattern


def get_all_urls(pass_lst=None):
    """
    获取项目中所有不在 pass_lst 中的url
    :param pass_lst: 不设权限的url，列表元素为url_name
    :return ret_lst: 返回的列表-结果
    """
    pass_lst = pass_lst or []
    ret_lst = []

    main_url_module =  importlib.import_module(settings.ROOT_URLCONF)
    main_urlpatterns = getattr(main_url_module, 'urlpatterns', None)

    if isinstance(main_urlpatterns, (list, tuple)):
        get_patterns_urls(main_urlpatterns, ret_lst=ret_lst, app_namespace=None, app_url=None, pass_lst=pass_lst)
        return ret_lst
    else:
        raise TypeError('[Project] > urls.py > urlpatterns must be a callable or a list/tuple.')


def get_patterns_urls(urlpatterns_lst, ret_lst, app_namespace=None, app_url=None, pass_lst=None):
    """
    基于回溯获取一个 patterns 中的所有 url
    :param urlpatterns_lst: 当前 urlpatterns 列表
    :param ret_lst: 返回的列表-结果
    :param app_namespace: app_命名空间
    :param app_url: app_前缀url
    :param pass_lst: 过滤列表
    :return: None
    """
    for url_obj in urlpatterns_lst:
        if isinstance(url_obj, URLResolver):
            app_urlpatterns = getattr(url_obj.urlconf_module, 'urlpatterns', None)
            if app_urlpatterns:
                get_patterns_urls(app_urlpatterns, ret_lst, url_obj.namespace, url_obj.pattern, pass_lst)
            else:
                raise NameError('{}(app) > urls.py > [url_lst] must be named to urlpatterns.'.format(url_obj.app_name))
        elif isinstance(url_obj, URLPattern):
            full_url_pattern = app_url._regex + url_obj.pattern._regex.replace('^', '').replace('$',  '') if app_url else url_obj.pattern._regex

            if url_obj.name:
                full_url_name = '{}:{}'.format(app_namespace, url_obj.name) if app_namespace else url_obj.name
            else:
                url_info = '{}(namespace) > {}'.format(app_namespace, url_obj.pattern._regex) if app_namespace else url_obj.pattern._regex
                raise ValueError('{} must set a url_name'.format(url_info))

            if full_url_name not in pass_lst:
                ret_lst.append({
                    'name': full_url_name,
                    'pattern': full_url_pattern,
                })
        else:
            raise TypeError('all object must be a URLResolver or a URLPattern in the urlpatterns_lst.')


if __name__ == '__main__':
    pass_lst = ['CRM:page_lst2', 'stella']
    ret = get_all_urls(pass_lst=pass_lst)

    for d in ret:
        print(d)
