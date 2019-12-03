from django.apps import AppConfig
from Web_CRM import settings

class CrmConfig(AppConfig):
    name = 'crm'


# UserInfo-Session KeyName (Session键名，可指向外部 str)
UserSessionKeyName ='Usess'


# Login白名单 (写入不需要经过登录校验的url, 可指定外部 URL_List)
LoginWhiteList = settings.URL_WHITE_LST