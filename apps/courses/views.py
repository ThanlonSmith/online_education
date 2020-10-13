from django.shortcuts import render
from .models import CourseInfo
from ..operations.models import UserLove, UserCourse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# 课程列表
def course_list(request):
    if request.method == "GET":
        page_num = request.GET.get('page_num', '')
        sort = request.GET.get('sort', '')
        """
        # 最新课程（按照时间倒序排序）
        all_courses = CourseInfo.objects.order_by('-add_time').all()
        """
        all_courses = CourseInfo.objects.all().order_by('-add_time')
        """
        # 热门课程推荐（按照学习人数倒序排序）
        recommend_courses = CourseInfo.objects.order_by('-study_num')[:2] # 不加.all()也是可以的
        """
        recommend_courses = all_courses.order_by('-study_num')[:2]
        """
        热门程度（按照课程的点击量倒序排序）
        参与人数（按照学习人数倒序排序）
        """
        if sort:
            all_courses = all_courses.order_by('-' + sort)
        """
        分页功能
        """
        per_page = 2
        paginator = Paginator(all_courses, per_page)
        num_pages = paginator.num_pages
        try:
            pages = paginator.page(page_num)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(1)
        return render(request, 'courses/course_list.html', {
            'all_courses': all_courses,
            'recommend_courses': recommend_courses,
            'pages': pages,
            'num_pages': num_pages,
            'sort': sort
        })


# 课程详情
def course_detail(request, course_id):
    if request.method == "GET":
        if course_id:
            current_course = CourseInfo.objects.filter(id=course_id)
            if current_course.exists():
                current_course = current_course.first()
                relate_course = CourseInfo.objects.filter(category=current_course.category).exclude(
                    id=course_id)[:2]  # <QuerySet []>
                # 判断机构和课程是否被当前用户收藏
                print(request.user.is_authenticated)  # True or False
                if request.user.is_authenticated:
                    org_love, course_love = False, False
                    if UserLove.objects.filter(love_man=request.user, love_id=current_course.org_info.id, love_type=1,
                                               love_status=True).exists():
                        org_love = True
                    if UserLove.objects.filter(love_man=request.user, love_id=course_id, love_type=2,
                                               love_status=True).exists():
                        course_love = True
                    return render(request, 'courses/course_detail.html', {
                        'current_course': current_course,
                        'relate_course': relate_course,
                        'org_love': org_love,
                        'course_love': course_love
                    })


# 课程视频
def course_video(request, course_id):
    if course_id:
        current_course = CourseInfo.objects.filter(id=course_id)
        if current_course.exists():
            current_course = current_course.first()
            """
            学习过该课程的用户
            """
            user_course = UserCourse.objects.filter(study_man=request.user, study_course=current_course)
            if not user_course.exists():
                uc = UserCourse()
                uc.study_man = request.user
                uc.study_course = current_course
                uc.save()
            """
            学习过该课的同学还学过什么课程
            """
            # course_list = [j.study_course for j in (user.usercourse_set.all() for user in user_list)]
            # print(course_list)
            # 分别获取每个用户课程，然后去掉重复的课程，包括当前的课程
            # 1、从中间表“用户课程表”中找到学习过该课程的所有用户课程列表
            user_course_list = UserCourse.objects.filter(
                study_course=current_course)  # user_course_list = current_course.usercourse_set.all()
            # 2、拿到学习过该们课程的用户列表
            user_list = [user_course.study_man for user_course in user_course_list]
            # 3、获取这些用户学过的课程，去除当前学过的课程
            user_course_list = UserCourse.objects.filter(study_man__in=user_list).exclude(study_course=current_course)
            # 4、获取其它课程
            course_list = list(set([user_course.study_course for user_course in user_course_list]))
            return render(request, 'courses/course_video.html', {
                'current_course': current_course,
                'course_list': course_list
            })


# 课程评论
def course_comment(request, course_id):
    current_course = CourseInfo.objects.filter(id=course_id)
    if current_course.exists():
        current_course = current_course.first()
        """
        学习过该课的同学还学过什么课程
        """
        # course_list = [j.study_course for j in (user.usercourse_set.all() for user in user_list)]
        # print(course_list)
        # 分别获取每个用户课程，然后去掉重复的课程，包括当前的课程
        # 1、从中间表“用户课程表”中找到学习过该课程的所有用户课程列表
        user_course_list = UserCourse.objects.filter(
            study_course=current_course)  # user_course_list = current_course.usercourse_set.all()
        # 2、拿到学习过该们课程的用户列表
        user_list = [user_course.study_man for user_course in user_course_list]
        # 3、获取这些用户学过的课程，去除当前学过的课程
        user_course_list = UserCourse.objects.filter(study_man__in=user_list).exclude(study_course=current_course)
        # 4、获取其它课程
        course_list = list(set([user_course.study_course for user_course in user_course_list]))
    return render(request, 'courses/course_comment.html', {
        'current_course': current_course,
        'course_list':course_list,
    })
