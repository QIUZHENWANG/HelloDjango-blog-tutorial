'''
Author:wqs
Date:2021年01月14日
Function:将模型注册到admin后台并美化
'''
from django.contrib import admin
from .models import Comment

# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    '''评论模型后台管理设置'''
    
    #显示字段设置
    list_display = ['name', 'email', 'url', 'post', 'created_time']
    
    #填写字段设置
    fields = ['name', 'email', 'url', 'text', 'post']
    
admin.site.register(Comment, CommentAdmin)