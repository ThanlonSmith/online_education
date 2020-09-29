import xadmin
from .models import BannerInfo, EmailVerifyCode
from xadmin import views


# 配置xadmin主题时，注册的时候要用专用的view去注册
class BaseXadminSetting:
    enable_themes = True
    use_bootswatch = True


class CommXadminSetting:
    site_title = '在线教育后台管理系统'
    site_footer = 'pythoneers.cn'
    menu_style = 'accordion'


class BannerInfoXadmin(object):
    list_display = ['image', 'url', 'add_time']
    # 设置过滤规则
    search_fields = ['image', 'url']
    list_filter = ['image', 'url']


class EmailVerifyCodeXadmin(object):
    list_display = ['code', 'email', 'send_type', 'add_time']


xadmin.site.register(BannerInfo, BannerInfoXadmin)
xadmin.site.register(EmailVerifyCode, EmailVerifyCodeXadmin)
# 注册主题类，注册xadmin主题
xadmin.site.register(views.BaseAdminView, BaseXadminSetting)
# 注册全局样式类，注册xadmin的标题和底部版权栏名称
xadmin.site.register(views.CommAdminView, CommXadminSetting)
