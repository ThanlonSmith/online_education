from django.apps import AppConfig


class CoursesConfig(AppConfig):
    name = 'apps.courses'
    # 在xadmin中显示中文，而不是英文
    verbose_name = '课程管理'
