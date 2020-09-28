from django.apps import AppConfig


class OrgsConfig(AppConfig):
    # name = 'orgs'
    """
    如果写了apps，导入的时候就可以：from apps.orgs.models import *
    并且不需要把apps下的app模块(courses等)设置Sources Root
    """
    name = 'apps.orgs'
