import xadmin
from .models import UserAsk, UserLove, UserCourse, UserComment, UserMessage


class UserAskXadmin:
    pass
    model_icon = 'fa fa-user'


class UserLoveXadmin:
    pass


class UserCourseXadmin:
    list_display = ['study_man', 'study_course', 'add_time']


class UserCommentXadmin:
    pass


class UserMessageXadmin:
    pass


xadmin.site.register(UserAsk, UserAskXadmin)
xadmin.site.register(UserLove, UserLoveXadmin)
xadmin.site.register(UserCourse, UserCourseXadmin)
xadmin.site.register(UserComment, UserCommentXadmin)
xadmin.site.register(UserMessage, UserMessageXadmin)
