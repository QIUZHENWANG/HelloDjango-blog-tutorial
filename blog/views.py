import markdown
import re
from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
# Create your views here.



def index(request):
    '''首页展示所有文章的简易信息列表'''
    
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={'post_list' : post_list})

def detail(request, pk):
    '''详细页展示特定文章的内容'''
    
    #存在即取，不存在则返回404页面
    post = get_object_or_404(Post, pk=pk)
    
    #支持markdown格式文章
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        
        #slugify支持标题中文
        TocExtension(slugify=slugify),
    ])
    
    #将Markdown文本解析成html文本，实例md会多出一个toc属性
    post.body = md.convert(post.body)
    
    #使用正则表达式去匹配生成的目录中包裹在 ul 标签中的内容
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''
    
    return render(request, 'blog/detail.html', context={'post' : post})

def archive(request, year, month):
    '''归档页展示特定年月的全部文章列表'''
    
    #使用过滤器filter筛选
    post_list = Post.objects.filter(created_time__year=year, created_time__month=month)
    return render(request, 'blog/index.html', context={'post_list': post_list})
    
def category(request, pk):
    '''分类页展示特定分类的全部文章列表'''
    
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list': post_list})
    
def tag(request, pk):
    '''标签页展示特定标签的全部文章列表'''
    
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t)
    return render(request, 'blog/index.html', context={'post_list': post_list})