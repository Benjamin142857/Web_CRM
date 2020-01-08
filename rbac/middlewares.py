from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, render
import rbac.apps as rbac_settings
from rbac.core import RbacManager


class RbacMiddleware(MiddlewareMixin):
    # Rbac权限校验
    # Rbac权限校验 -> 组件加工 -> 生成RbacManager
    def process_view(self, request, view_func, view_args, view_kwargs):
        # 只对非白名单内url进行
        if request.path_info not in rbac_settings.RbacWhiteList:
            # 0. 校验是否有init_permission
            RbacSession = request.session.get(rbac_settings.RbacSessionKeyName)
            if not RbacSession:
                raise ValueError('Rbac Session 不存在， 请确保非白名单内 url 访问前已进行 init_permission.')

            # 1. 权限校验
            Permissions = RbacSession['Permissions']
            # 1.1 通过校验, 生成RbacManager
            if request.path_info in Permissions.keys:
                rbac_manager = RbacManager()
            # 1.2 无权限，返回无权限页面
            else:
                return render(request, rbac_settings.RbacNoPermissionHTML)

            # 2. 隶属关系生成
            now_url_info_dct = Permissions[request.path_info]
            relationship_lst = []
            # 3.1 有父级，三级菜单
            if now_url_info_dct.get('MenuParent_path'):
                relationship_lst.extend([now_url_info_dct['MenuParent_path']['MenuRoot_id'], now_url_info_dct['MenuParent_path']['url_path'], now_url_info_dct['url_path']])
            # 3.2 无父级有根级，二级菜单
            elif now_url_info_dct.get('MenuRoot_id'):
                relationship_lst.extend([now_url_info_dct['MenuRoot_id'], now_url_info_dct['url_path']])
            # 3.3 无父级无根级，未分类，不考虑
            else:
                pass

        # 3. 三级动态菜单加选中类
            ThreeLayerMenu = rbac_settings.InclusionConfig.get('ThreeLayerMenu') and RbacSession.get('ThreeLayerMenu')
            if ThreeLayerMenu:
                node = ThreeLayerMenu
                # 3.1 ThreeLayerMenu 基于 relationship_lst 逐级加入active
                for child in relationship_lst:
                    node = node[child]
                    node['class'] = 'active'
                rbac_manager.ThreeLayerMenu = ThreeLayerMenu

            # 4. 基于动态菜单的面包屑导航生成
            if rbac_settings.InclusionConfig.get('BreadCrumb'):
                BreadCrumb = []
                # 4.1 先生成根菜单
                BreadCrumb.append({
                    'label': Permissions[relationship_lst[1]['MenuRoot_label']],
                })

                # 4.2 基于 relationship_lst 逐级生成
                for child in relationship_lst[1:]:
                    BreadCrumb.append({
                        'label': Permissions[child]['label'],
                        'url': Permissions[child]['url_path'],
                    })
                rbac_manager.BreadCrumb = BreadCrumb

            # request加入RbacManager
            request.RbacManager = rbac_manager
