from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from django.shortcuts import reverse, redirect
from crm import apps as crm_settings
from rbac.models import UserProfile

class CrmMiddleware(MiddlewareMixin):
    # 登录校验
    def process_view(self, request, view_func, view_argsm, view_kwargs):
        user_id = request.session.get(crm_settings.UserSessionKeyName)

        # 白名单或已登录，PASS
        if (request.path_info in crm_settings.LoginWhiteList) or user_id:
            request.UserObj = UserProfile.objects.filter(id=user_id).first() if user_id else None
            return None
        # 跳转登录界面,并记录下当前信息
        else:
            return redirect(reverse('login') + '?next={}'.format(request.path_info))
