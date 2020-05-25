from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.html import strip_tags
import markdown
# Create your models here.
class Category(models.Model):

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
    name = models.CharField(max_length=100)


class Tag(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name

class Post(models.Model):

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def save(self, *args,**kwargs):
        self.modified_time = timezone.now()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(self.body)[:54]
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})
    title = models.CharField("标题",max_length=70)
    body = models.TextField('正文')

    created_time = models.DateTimeField('创建时间',default=timezone.now)
    modified_time = models.DateTimeField('修改时间',default=timezone.now)
    #摘要
    excerpt = models.CharField('摘要',max_length=200,blank=True)
    category = models.ForeignKey(Category,verbose_name="分类",on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag,verbose_name="标签",blank=True)

    author = models.ForeignKey(User,on_delete=models.CASCADE)
    
