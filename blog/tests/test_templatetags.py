from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Post, Category, Tag
from django.template import Context, Template
from ..templatetags.blog_extras import show_recent_posts

class TemplatetagsTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_superuser(
            username='admin', 
            email='admin@hellogithub.com', 
            password='admin')
        cate = Category.objects.create(name='测试')
        self.post = Post.objects.create(
            title='测试标题',
            body='测试内容',
            category=cate,
            author=user,
        )
        self.ctx = Context()
    def test_show_recent_posts_with_posts(self):
        context = Context(show_recent_posts(self.ctx))
        template = Template(
            '{% load blog_extras %}'
            '{% show_recent_posts %}'
        )
     
        expected_html = template.render(context)
        self.assertInHTML('<h3 class="widget-title">最新文章</h3>', expected_html)
        self.assertInHTML('<a href="{}">{}</a>'.format(self.post.get_absolute_url(), self.post.title), expected_html)