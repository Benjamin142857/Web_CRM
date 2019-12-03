from django.utils.deprecation import MiddlewareMixin
from crm import apps as crm_settings
from django.http import HttpResponse
from django.shortcuts import reverse

class CrmMiddleware(MiddlewareMixin):
    # 登录校验
    def process_request(self, request):
        request.UserObj = request.session.get(crm_settings.UserSessionKeyName)

        # 白名单或已登录，PASS
        if (request.path_info in crm_settings.LoginWhiteList) or request.UserObj:
            pass
        # 跳转登录界面,并记录下当前信息
        else:
            pass
