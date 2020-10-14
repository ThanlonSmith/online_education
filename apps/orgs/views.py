from django.shortcuts import render
from .models import OrgInfo, CityInfo
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from ..operations.models import UserLove
from .models import TeacherInfo


# Create your views here.
# 机构列表
def org_list(request):
    all_orgs = OrgInfo.objects.all()
    """
    print(all_orgs)  # <QuerySet [<OrgInfo: 北京大学>, <OrgInfo: 清华大学>, <OrgInfo: 复旦大学>, <OrgInfo: 慕课网>]>
    """
    all_citys = CityInfo.objects.all()
    # 根据授课机构的收藏量为依据排名，取前5条排序好的数据
    ranking_orgs = OrgInfo.objects.order_by("-love_num")[:5]
    # 获取url上的页码
    page_num = request.GET.get('page_num', '')
    """
    根据机构类别进行帅选
    """
    category = request.GET.get('category', '')  # <class 'str'>
    if category:
        all_orgs = all_orgs.filter(category=category)
    """
    根据所在地区进行刷选
    """
    city_id = request.GET.get('city_id', '')
    if city_id:
        all_orgs = all_orgs.filter(city_info_id=int(city_id))
    """
    排序
    """
    sort = request.GET.get('sort', '')
    if sort:
        all_orgs = all_orgs.order_by('-' + sort)
    """
    分页
    """
    # 创建分页对象，指定每页显示的数据条数
    per_page_num = 6
    # 创建分页对象
    paginator = Paginator(all_orgs, per_page_num)
    try:
        pages = paginator.page(page_num)
    except PageNotAnInteger:
        pages = paginator.page(1)  # # 如果传入的页码不是整型，则默认显示第一页，如传入的是/student.html/?page=abc，/student.html/
    except EmptyPage as e:
        # pages = paginator.page(paginator.num_pages)
        pages = paginator.page(1)  # 如果传入的页码是空页，则默认显示第一页。如传入的是/student.html/?page=-10
    return render(request, 'orgs/orgs_list.html', {
        # 'all_orgs': all_orgs,
        'pages': pages,
        'all_citys': all_citys,
        'ranking_orgs': ranking_orgs,
        # 总的页码数
        'sum_page_num': paginator.num_pages,
        # 总的数据量
        'sum_count': paginator.count,
        # 分类
        'category': category,
        'city_id': city_id,
        'sort': sort
    })


# 机构首页
def org_home(request, org_id):
    print(type(org_id))  # <class 'str'>
    # curr_org = OrgInfo.objects.filter(id=org_id).first()
    curr_org = OrgInfo.objects.filter(id=org_id)[0]
    # 当前机构的课程，维护数据
    curr_org_courses = curr_org.courseinfo_set.all()[:2]
    curr_org_teachers = curr_org.teacherinfo_set.all()[:1]
    # 需要返回收藏机构的状态
    love_status = False
    if request.user.is_authenticated:
        love = UserLove.objects.filter(love_man=request.user, love_id=org_id, love_type=1, love_status=True)
        if love.exists():
            love_status = True
    return render(request, 'orgs/org_home.html', {
        'curr_org': curr_org,
        'menu_title': 'org_home',
        'curr_org_courses': curr_org_courses,
        'curr_org_teachers': curr_org_teachers,
        'love_status': love_status
    })


# 机构课程
def org_course(request, org_id):
    curr_org = OrgInfo.objects.filter(id=org_id).first()
    # 当前机构的所有课程
    curr_org_courses = curr_org.courseinfo_set.all()
    # 分页功能
    page_num = request.GET.get('page_num', '')
    paginator = Paginator(curr_org_courses, 2)
    # 获取总的页码数
    num_pages = paginator.num_pages
    # 需要返回收藏机构的状态
    love_status = False
    if request.user.is_authenticated:
        love = UserLove.objects.filter(love_man=request.user, love_id=org_id, love_type=1, love_status=True)
        if love.exists():
            love_status = True
    try:
        pages = paginator.page(page_num)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        # paginator.num_pages：总页数
        pages = paginator.page(num_pages)
    return render(request, 'orgs/org_course.html', {
        'curr_org': curr_org,
        'menu_title': 'org_course',
        'pages': pages,
        'num_pages': num_pages,
        'love_status': love_status
    })


# 机构介绍
def org_desc(request, org_id):
    curr_org = OrgInfo.objects.filter(id=org_id).first()
    # 需要返回收藏机构的状态
    love_status = False
    if request.user.is_authenticated:
        love = UserLove.objects.filter(love_man=request.user, love_id=org_id, love_type=1, love_status=True)
        if love.exists():
            love_status = True
    return render(request, 'orgs/org_desc.html', {
        'curr_org': curr_org,
        'menu_title': 'org_desc',
        'love_status': love_status
    })


# 机构讲师
def org_teacher(request, org_id):
    curr_org = OrgInfo.objects.filter(id=org_id).first()
    curr_org_teachers = curr_org.teacherinfo_set.all()
    page_num = request.GET.get('page_num', '')
    paginator = Paginator(curr_org_teachers, 2)
    num_pages = paginator.num_pages
    # 需要返回收藏机构的状态
    love_status = False
    if request.user.is_authenticated:
        love = UserLove.objects.filter(love_man=request.user, love_id=org_id, love_type=1, love_status=True)
        if love.exists():
            love_status = True
    try:
        pages = paginator.page(page_num)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(num_pages)
    return render(request, 'orgs/org_teacher.html', {
        'curr_org': curr_org,
        'menu_title': 'org_teacher',
        'pages': pages,
        'num_pages': num_pages,
        'love_status': love_status
    })


# 讲师列表
def teacher_list(request):
    # 讲师排行榜，根据收藏数量
    ranking_list = TeacherInfo.objects.order_by('-love_num')[:2]
    all_teacher = TeacherInfo.objects.all()
    sort = request.GET.get('sort', '')
    # 讲师排行榜，根据点击数量
    if sort:
        all_teacher = TeacherInfo.objects.order_by('-' + sort)
    page_num = request.GET.get('page_num', '')
    paginator = Paginator(all_teacher, per_page=2)
    num_pages = paginator.num_pages
    try:
        pages = paginator.page(page_num)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(num_pages)
    return render(request, 'orgs/teacher_list.html', {
        'ranking_list': ranking_list,
        'pages': pages,
        'sort': sort,
        'num_pages': num_pages
    })


# 讲师详情
def teacher_detail(request, teacher_id):
    ranking_list = TeacherInfo.objects.order_by('-love_num')[:2]
    current_teacher = TeacherInfo.objects.filter(id=teacher_id)
    if current_teacher.exists():
        current_teacher = current_teacher[0]
    return render(request, 'orgs/teacher_detail.html', {
        'ranking_list': ranking_list,
        'current_teacher': current_teacher
    })
