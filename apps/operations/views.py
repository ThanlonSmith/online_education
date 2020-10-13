from .forms import UserAskForm
from django.http import JsonResponse
from apps.operations.models import UserLove, UserComment
from .forms import UserCommentForm
from apps.courses.models import CourseInfo


# 用户咨询
def user_ask(request):
    ret = {'status': None, 'msg': None}
    if request.method == 'POST':
        user_ask_form = UserAskForm(request.POST)
        if user_ask_form.is_valid():
            """
            使用user_ask_form调用save方法就会保存model，不需要获取数据后创建model类保存，字段比较多的情况下非常简便！
            """
            user_ask_form.save(commit=True)
            ret['status'] = 'ok'
            ret['msg'] = '咨询成功！'
            return JsonResponse(ret)
        else:
            ret['status'] = 'fail'
            ret['msg'] = '咨询失败，请检查您输入的内容！'
            return JsonResponse(ret)


# 用户收藏
def user_love(request):
    ret = {'status': None, 'msg': None}
    if request.method == 'GET':
        love_id = request.GET.get('love_id', '')
        love_type = request.GET.get('love_type', '')
        if love_id and love_type:
            # 查看用户是否已经收藏过
            user_love = UserLove.objects.filter(love_id=love_id, love_type=love_type, love_man=request.user)
            # user_love_first = user_love.first()
            if user_love.exists():
                user_love_first = user_love[0]
                # 如果用户已经收藏，这次是取消收藏
                if user_love_first.love_status:
                    user_love_first.love_status = False
                    user_love_first.save()
                    ret['status'] = 'ok'
                    ret['msg'] = '收藏'
                else:
                    user_love_first.love_status = True
                    user_love_first.save()
                    ret['status'] = 'ok'
                    ret['msg'] = '取消收藏'
            else:
                ul = UserLove()
                ul.love_id = love_id
                ul.love_man = request.user
                ul.love_type = love_type
                ul.love_status = True
                ul.save()
                ret['status'] = 'ok'
                ret['msg'] = '取消收藏'
        else:
            pass
    else:
        pass
    return JsonResponse(ret)


# 课程评论
def course_comment(request):
    if request.method == 'POST':
        ret = {'status': None, 'msg': None}
        user_comment_form = UserCommentForm(request.POST)
        if user_comment_form.is_valid():
            course_id = user_comment_form.cleaned_data['course_id']
            comment_content = user_comment_form.cleaned_data['comment_content']
            if course_id and comment_content:
                course_info = CourseInfo.objects.filter(id=course_id)
                if course_info.exists():
                    course_info = course_info.first()
                    uc = UserComment()
                    uc.comment_course = course_info
                    uc.comment_content = comment_content
                    uc.comment_man = request.user
                    uc.save()
                    ret['status'] = 'ok'
                    ret['msg'] = '评论成功！'
        else:
            ret['status'] = 'fail'
            ret['msg'] = '评论失败！'
        return JsonResponse(ret)
