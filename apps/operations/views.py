from .forms import UserAskForm
from django.http import JsonResponse


# Create your views here.
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
