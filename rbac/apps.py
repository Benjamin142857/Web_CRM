from django.apps import AppConfig


class RbacConfig(AppConfig):
    name = 'rbac'


# RBAC对应的用户表配置
ModelUserConfig = {
    'UserModel': 'rbac.models.UserProfile',
    'UserRoleField': 'role',
}


# RBAC 组件库配置
InclusionConfig = {
    # 基于当前角色的动态三级菜单
    'ThreeLayerMenu': {

    },

    # 基于动态菜单的面包屑导航
    'BreadCrumb': {

    },
}

DEBUG = True