from django.shortcuts import render
from .models import CourseInfo
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
