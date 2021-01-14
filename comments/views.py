'''
Author:wqs
Date:2021年01月14日
Function:评论视图函数
'''
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from django.views.decorators.http import require_POST
from .forms import CommentForm
from django.contrib import messages


# Create your views here.

@require_POST
def comment(request, post_pk):
    '''评论表单处理逻辑'''
    
    #获取被评论文章
    post = get_object_or_404(Post, pk=post_pk)
    form = CommentForm(request.POST)
    
    #调用 form.is_valid() 检查表单的数据是否符合格式要求
    if form.is_valid():
        # save 方法保存数据到数据库
        # commit=False 的作用是生成 Comment 模型类的实例，但还不保存评论数据到数据库。
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        
        #使用 django 自带的 messages 应用来给用户发送评论成功或者失败的消息
        messages.add_message(request, messages.SUCCESS, '评论发表成功！', extra_tags='success')
        
        #重定向到 post 中 get_absolute_url 方法返回的 URL
        return redirect(post)
    
    context = {
        'post': post,
        'form': form,
    }
    messages.add_message(request, messages.ERROR, '评论发表失败！请修改表单中的错误后重新提交', extra_tags='danger')
    return render(request, 'comments/preview.html', context=context)