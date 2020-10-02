from django.shortcuts import render
from .models import OrgInfo, CityInfo
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.
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
    per_page_num = 4
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
