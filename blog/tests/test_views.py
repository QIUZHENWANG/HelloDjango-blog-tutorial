from django.test import TestCase
from django.utils import timezone
from ..models import Post, Category, Tag
from django.shortcuts import reverse
from django.contrib.auth.models import User
from  datetime import timedelta

class BlogDateTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username = 'admin',
            email = 'admin@hellogithub.com',
            password = 'admin'
        )
        
        self.cate1 = Category.objects.create(name='测试分类1')
        self.cate2 = Category.objects.create(name='测试分类2')
        
        self.tag1 = Tag.objects.create(name='测试标签1')
        self.tag2 = Tag.objects.create(name='测试标签2')
        
        self.post1 = Post.objects.create(
            title = '测试标题一',
            body='测试内容一',
            category = self.cate1,
            author = self.user
        )
        self.post1.tags.add(self.tag1)
        self.post1.save()
        
        self.post2 = Post.objects.create(
            title = '测试标题二',
            body = '测试内容二',
            category=self.cate2,
            author=self.user,
            created_time=timezone.now() - timedelta(days=100)
        )
        
class CategoryViewTestCase(BlogDateTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('blog:category',  kwargs={'pk': self.cate1.pk})
        self.url2 = reverse('blog:category', kwargs={'pk':self.cate2.pk})

    def test_visit_a_nonexistent_category(self):
        url = reverse('blog:category', kwargs={'pk': 100})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_without_any_post(self):
        Post.objects.all().delete()
        response = self.client.get(self.url2)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/index.html')
        self.assertContains(response, '暂时还没有发布的文章！')
        
    def test_with_posts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/index.html')
        self.assertContains(response, self.post1.title)
        self.assertIn('post_list', response.context)
        self.assertIn('is_paginated', response.context)
        self.assertIn('page_obj', response.context)
        self.assertEqual(response.context['post_list'].count(), 1)
        expected_qs = self.cate1.post_set.all().order_by('-created_time')
        self.assertQuerysetEqual(response.context['post_list'], [repr(p) for p in expected_qs])
    