from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save

from utils.id_utils import hashid

# Create your models here.

class MyUser(AbstractUser):
    '''
    用户的数据结构，继承 AbstractUser
    '''
    uid = models.CharField(max_length=32, default='', unique=True, editable=False) # 具有唯一性的用户ID
    created_at = models.DateTimeField(auto_now_add=True) # 用户创建的时间
    updated_at = models.DateTimeField(auto_now=True) # 用户信息最新变更的时间
    ac_rate = models.FloatField(default=1) # 用户答题的正确率

    class Meta:
        db_table = 'myuser' # 数据库表名称
        verbose_name = '用户'
        verbose_name_plural = '用户管理'

    def __str__(self): # 数据库中查询时返回用户名
        return self.username

@receiver(post_save, sender=MyUser, dispatch_uid='gen_myuser_uid')
def update_uid(sender, instance, **kwargs):
    if not instance.uid:
        instance.uid = hashid(instance.id, length=6) # 生成用户uid
        instance.save()
