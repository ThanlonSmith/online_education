import xadmin
from .models import CourseInfo, LessonInfo, VideoInfo, SourceInfo


class CourseInfoXadmin:
    list_display = ['image', 'name', 'study_time', 'study_num', 'level', 'love_num', 'click_num', 'desc', 'detail',
                    'category', 'course_notice', 'course_need', 'teacher_tell', 'org_info', 'teacher_info', 'is_banner',
                    'add_time']
    model_icon = 'fa fa-user'

class LessonInfoXadmin:
    list_display = ['name','course_info','add_time']

class VideoInfoXadmin:
    list_display = ['name','study_time','url','lesson_info','add_time']


class SourceInfoXadmin:
    list_display =['name','down_load','course_info','add_time']


xadmin.site.register(CourseInfo, CourseInfoXadmin)
xadmin.site.register(LessonInfo, LessonInfoXadmin)
xadmin.site.register(VideoInfo, VideoInfoXadmin)
xadmin.site.register(SourceInfo, SourceInfoXadmin)
