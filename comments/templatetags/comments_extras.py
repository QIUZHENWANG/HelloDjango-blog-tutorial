'''
Author:wqs
Date:2021年01月14日
Function:生成评论自定义模板标签
'''
from django import template
from ..forms import CommentForm

register = template.Library()

@register.inclusion_tag('comments/inclusions/_form.html', takes_context=True)
def show_comment_form(context, post, form=None):
    '''显示评论表单'''
    
    if form is None:
        form = CommentForm
    return {
        'form': form,
        'post': post,
    }
    
@register.inclusion_tag('comments/inclusions/_list.html', takes_context=True)
def show_comments(context, post):
    '''展示评论数量及内容'''
    
    #post.comment_set.all() 也等价于 Comment.objects.filter(post=post)
    comment_list = post.comment_set.all()
    comment_count = comment_list.count()
    return {
        'comment_count': comment_count,
        'comment_list': comment_list,
    }