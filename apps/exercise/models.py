from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from utils.id_utils import hashid
from apps.account.models import MyUser

# Create your models here.

class Question(models.Model):
    '''
    问题的数据结构，继承 models.Model
    '''
    qid = models.CharField(max_length=32, default='', unique=True, editable=False, verbose_name='题目ID') # 具有唯一性的问题ID
    content = models.CharField(max_length=35, default='', verbose_name='题面') # 问题的内容
    created_at = models.DateTimeField(auto_now_add=True) # 试题创建的时间
    updated_at = models.DateTimeField(auto_now=True) # 试题修改的时间
    user = models.ForeignKey(MyUser, null=True, on_delete=models.CASCADE, verbose_name='用户') # 将试题关联到用户，删除用户后需要删除该试题
    usrAns = models.CharField(max_length=15, default='', verbose_name='用户答案') # 用户填写的答案
    status = models.CharField(max_length=2, default='', verbose_name='判题结果') # 试题正确性
    correctAns = models.CharField(max_length=15, default='', verbose_name='正确答案') # 正确答案
    
    class Meta:
        db_table = 'question' # 数据库表名称
        verbose_name = '题目'
        verbose_name_plural = '题目管理'

    def __str__(self): # 在数据库中查询时返回题面内容
        return self.content


@receiver(post_save, sender=Question, dispatch_uid='gen_question_qid')
def update_qid(sender, instance, **kwargs):
    if not instance.qid:
        instance.qid = hashid(instance.id,length=8) # 注意这里是8位，而用户的uid是6位
        instance.save()
    