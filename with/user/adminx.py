import xadmin
from .models import *
from xadmin import views

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "With后台管理系统"
    site_footer = "With"
    menu_style = "accordion"

xadmin.site.register(EmailVerifyCode)
xadmin.site.register(Message)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)