'''
Author:wqs
Date:2021年01月14日
Function:建立数据库模型
'''
from django.db import models
from django.utils import timezone


# Create your models here.
class Comment(models.Model):
    '''评论模型，保存用户的姓名，邮箱，个人网站，评论内容，评论创建时间及关联的文摘'''
    
    name = models.CharField('名字', max_length=50)
    email = models.EmailField('邮箱')
    url = models.URLField('网址', blank=True)
    text = models.TextField('内容')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    
    #一文章可以有多评论
    post = models.ForeignKey('blog.Post', verbose_name='文章', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
    
    def __str__(self):
        return '{}: {}'.format(self.name, self.text[:20])