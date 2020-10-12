from django.shortcuts import render
from .models import CourseInfo
from ..operations.models import UserLove
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
