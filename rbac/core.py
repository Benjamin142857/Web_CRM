"""
    coding      : UTF-8
    Environment : Python 3.6
    Author      : Benjamin142857
    Data        : 12/2/2019
    Remark      : core
"""
# DEBUG
import os
import sys
import django
# add django root-path into environ / 将django项目根目录加入环境变量
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import django setting / 引入django配置文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Web_CRM.settings")
# setup django / 启动django
django.setup()


import importlib
from rbac import apps as rbac_settings
from rbac.models import Permission, Role, MenuRoot, UserProfile


class RbacManager(object):
    def __init__(self):
        self.a = 3


def init_permission(request, UserObj):
    # 0. 引入配置并校验, 获取用户角色QuerySet
    try:
        app, models, table = rbac_settings.ModelUserConfig['UserModel'].split('.')
        UserModel = getattr(importlib.import_module(app + '.' + models), table)
        # 0.1 校验 rbac_settings.ModelUserConfig['UserModel'] 配置
        if isinstance(UserObj, UserModel):
            UserRolesQS = getattr(UserObj, rbac_settings.ModelUserConfig['UserRoleField']).all()
            FirstRole = UserRolesQS.first()
            IsAdmin = getattr(UserObj, rbac_settings.ModelUserConfig['UserIsAdminField'])

            # 0.2 校验 rbac_settings.ModelUserConfig['UserRoleField'] 配置
            if not isinstance(FirstRole, (type(None), Role)):
                raise ValueError("rbac.apps.ModelUserConfig['UserRoleField'] 对应字段没有对应关联到 rbac.models.Role.")

            # 0.3 校验 rbac_settings.ModelUserConfig['UserRoleField'] 配置
            if not isinstance(IsAdmin, bool):
                raise ValueError("rbac.apps.ModelUserConfig['UserIsAdminField'] 对应字段非BooleanField类型，若已对应则可能是用户该字段为空，请补上默认值(True/False).")
        else:
            raise ValueError("rbac.apps.ModelUserConfig['UserModel'] 与 UserObj 传入对象表类型不一致, 注意需传入相应数据对象而非QuerySet.")

        # 0.4 校验Session

        # 初始化session_dct
        session_dct = {}
    except Exception:
        raise ValueError('rbac.apps 配置信息出错')

    # 1. 根据Role-QuerySet生成Perimission_dct
    if IsAdmin:
        Permission_dct = '__all__'
    else:
        Permission_dct = generate_Permissions_dct(UserRolesQS)
    session_dct['Permissions'] = Permission_dct


    # 2.1 基于当前角色的动态三级菜单
    ThreeLayerMenu = rbac_settings.InclusionConfig.get('ThreeLayerMenu')
    if ThreeLayerMenu:
        ThreeLayerMenu_dct = generate_ThreeLayerMenu_dct(UserRolesQS)
        session_dct['ThreeLayerMenu'] = ThreeLayerMenu_dct

    # 3. 写入Session
    request.session[rbac_settings.RbacSessionKeyName] = session_dct


def generate_Permissions_dct(UserRoleQS):
    all_perm_info_dct = UserRoleQS.values(
        'permissions__url_path',
        'permissions__url_name',
        'permissions__menu_root',
        'permissions__menu_parent__url_path',
        'permissions__label',
    ).distinct()

    Permissions_dct = {}
    for one_perm_info_dct in all_perm_info_dct:
        Permissions_dct[one_perm_info_dct['permissions__url_path']] = {
            'url_path': one_perm_info_dct['permissions__url_path'],
            'url_name': one_perm_info_dct['permissions__url_name'],
            'MenuRoot_id': one_perm_info_dct['permissions__menu_root'],
            'MenuParent_path': one_perm_info_dct['permissions__menu_parent__url_path'],
            'label': one_perm_info_dct['permissions__label'],
        }

    return Permissions_dct


def generate_ThreeLayerMenu_dct(UserRoleQS):
    ThreeLayerMenu_dct = {}
    perm_qs = Permission.objects.filter(Role__in=UserRoleQS if UserRoleQS.exists() else [])

    # 以g2为基准，循环逐级生成
    for g2_obj in perm_qs.filter(menu_root__isnull=False):

        # g2['children'] - all_g3_dct 生成
        all_g3_dct = {}
        for g3_obj in g2_obj.Children.all():
            all_g3_dct[g3_obj.url_path] = {
                'url_name': g3_obj.url_name,
                'label': g3_obj.label
            }

        # g2_dct 生成
        g2_dct = {
            'url_name': g2_obj.url_name,
            'label': g2_obj.label,
            'children': all_g3_dct,
        }

        # g2_dct 加入到 MenuRoot_dct 中
        MenuRoot_dct = ThreeLayerMenu_dct.get(str(g2_obj.menu_root.id))
        if MenuRoot_dct:
            MenuRoot_dct['children']['g2_obj.url_path'] = g2_dct
        else:
            ThreeLayerMenu_dct[str(g2_obj.menu_root.id)] = {
                'label': g2_obj.menu_root.label,
                'icon': g2_obj.menu_root.icon,
                'weight': g2_obj.menu_root.weight,
                'children': {g2_obj.url_path: g2_dct},
            }

    return ThreeLayerMenu_dct





if __name__ == '__main__':
    user = UserProfile.objects.filter(id=1).first()
    init_permission('a', user)