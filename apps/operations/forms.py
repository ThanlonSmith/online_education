from django import forms
from apps.operations.models import UserAsk
import re


# 通过Model的验证规则验证form使用ModelForm，要求必须和表中的字段名一样
class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        """
        使用所有字段
        """
        # fields = '__all__'
        """
        除了哪些字段，其它都用
        """
        # exclude = ['add_time']
        """
        使用部分字段(如果验证成功，放在cleaned_data中。还可以从cleaned_data中取出来再做一次验证)
        """
        fields = ['name', 'phone', 'course']  # 用model这三个字段做验证

    """
    还可以从cleaned_data中取出来再做一次验证
    """

    def clean_name(self):
        name = self.cleaned_data['name']
        return name

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        com = re.compile('^1([358][0-9]|4[579]|66|7[0135678]|9[89])[0-9]{8}$')
        if com.match(phone):
            return phone
        else:
            raise forms.ValidationError('手机号不合法！ ')
            # form对象_errors中
            """
            form对象_errors中
            <ul class="errorlist"><li>phone<ul class="errorlist"><li>手机号不合法！ </li></ul></li></ul>
            """

    def clean_course(self):
        course = self.cleaned_data['course']
        return course
