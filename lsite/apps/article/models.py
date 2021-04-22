from django.db import models
from django.urls import reverse

from taggit.managers import TaggableManager
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
import uuid,os


# Create your models here.


# def user_directory_path(instance, filename):
#     ext = filename.split('.')[-1]
#     filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
#     return os.path.join('user', "editor", filename)


class Article(models.Model):
    title = models.CharField('标题', max_length=100)
    body = models.TextField(verbose_name='正文')
    avatar = ProcessedImageField(verbose_name='配图', upload_to='articles/%Y/%m/%d/',
                                 blank=True, null=True, format='JPEG',
                                 options={'quality': 100},)
    created = models.DateField('创建日期', auto_now_add=True)
    updated = models.DateField('修改日期', auto_now=True)
    total_views = models.PositiveIntegerField('浏览量', default=0)
    tags = TaggableManager('标签')
    supports = models.PositiveIntegerField('点赞量', default=0)
    isPrivate = models.BooleanField('是否私密',default=False)

    def __str__(self):
        return self.title

    #def get_absolute_url(self):
        #return reverse('notes:note-detail',args=[self.id])


    class Meta:
        db_table = 'tb_articles'
        ordering = ['-updated']
        verbose_name = '文章'
        verbose_name_plural = verbose_name
