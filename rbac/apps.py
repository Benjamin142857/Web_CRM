from django.apps import AppConfig
from django.shortcuts import render
from Web_CRM import settings


class RbacConfig(AppConfig):
    name = 'rbac'


# RBAC 对应的用户表配置
ModelUserConfig = {
    'UserModel': 'rbac.models.UserProfile',         # value填入相应表名-按格式("app.models.TableName")
    'UserRoleField': 'role',                        # value填入相应字段名
    'UserIsAdminField': 'IsAdmin',                  # value填入相应字段名
}

# RBAC-Session KeyName (Session键名，可指向外部 str)
RbacSessionKeyName ='Rsess'

# RBAC 权限白名单 (写入不需要经过权限校验的url, 可指定外部 URL_List)
RbacWhiteList = settings.URL_WHITE_LST

# RBAC 无权限返回页面
RbacNoPermissionHTML = 'rbac/templates/NoPermission.html'

# RBAC 组件库配置
InclusionConfig = {
    'ThreeLayerMenu': True,     # 基于当前角色的动态三级菜单
    'BreadCrumb': True,         # 基于动态菜单的面包屑导航
}
