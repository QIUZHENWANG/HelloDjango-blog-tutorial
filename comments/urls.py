'''
Author:wqs
Date:2021年01月14日
Function:生成评论 url 模式
'''
from django.urls import path
from . import views

app_name = 'comments'
urlpatterns = [
    path('comment/<int:post_pk>', views.comment, name='comment'),
]