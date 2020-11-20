from django.contrib import admin

from apps.account.models import MyUser
from apps.exercise.models import Question

# Register your models here.

class QuestionInline(admin.TabularInline):
    '''
    将题目内联到用户管理中
    '''
    model = Question

class MyUserAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('uid', 'username', 'is_active', 'is_staff')

admin.site.register(MyUser, MyUserAdmin)