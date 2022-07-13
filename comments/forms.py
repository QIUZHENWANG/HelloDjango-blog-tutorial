'''
Author:wqs
Date:2021年01月14日
Function:生成表单收集数据
'''
from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    '''评论表单设置'''
    
    class Meta:
    
        #指定表单对应的数据库模型
        model = Comment
        
        #指定表单需要显示的字段
        fields = ['name', 'email', 'url', 'text']