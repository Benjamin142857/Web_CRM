from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
import rbac.apps as rbac_settings
from rbac.core import RbacManager


class RbacMiddleware(MiddlewareMixin):
    # Rbac权限校验
    def process_request(self, request):
        # 1. request.在白名单内
            # 1.1 PASS
        # 2. 不在白名单内
        pass

    # RbacManager生成, 组件加工
    def process_view(self, request, view_func, view_args, view_kwargs):
        # 只对非白名单内url进行
        if request.path_info not in rbac_settings.RbacWhiteList:
            # 0. 校验是否有init_permission
            RbacSession = request.session.get(rbac_settings.RbacSessionKeyName)
            if not RbacSession:
                raise ValueError('Rbac Session 不存在， 请确保非白名单内 url 访问前已进行 init_permission.')

            Permissions = RbacSession.get('Permission')
            ThreeLayerMenu = rbac_settings.InclusionConfig.get('ThreeLayerMenu') and RbacSession.get('ThreeLayerMenu')
            BreadCrumb = rbac_settings.InclusionConfig.get('BreadCrumb') and RbacSession.get('BreadCrumb')
            rbac_manager = RbacManager()

            # 1. 三级动态菜单生成
            if ThreeLayerMenu:
                pass

            # 2. 基于动态菜单的面包屑导航生成
            if BreadCrumb:
                pass


            # request加入RbacManager
            request.RbacManager = rbac_manager
