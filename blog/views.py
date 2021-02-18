import markdown
import re
from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.views.generic import ListView, DetailView
from pure_pagination.mixins import PaginationMixin

# Create your views here.


class IndexView(PaginationMixin, ListView):
    '''首页展示所有文章的简易信息列表'''
    
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 5


class PostDetailView(DetailView):
    '''详细页展示特定文章的内容'''

    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    
    # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
    # get 方法返回的是一个 HttpResponse 实例
    # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
    # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        
        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()
        
        # 视图必须返回一个 HttpResponse 对象
        return response
    
    # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
    def get_object(self, queryset=None):
        post = super().get_object(queryset=None)
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
        return post
        
class ArchiveView(IndexView):
    '''归档页展示特定年月的全部文章列表'''

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchiveView, self).get_queryset().filter(created_time__year=year, created_time__month=month)
    
class CategoryView(IndexView):
    '''分类页展示特定分类的全部文章列表'''
    
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

class TagView(IndexView):
    '''标签页展示特定标签的全部文章列表'''
    
    def get_queryset(self):
        t = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=t)