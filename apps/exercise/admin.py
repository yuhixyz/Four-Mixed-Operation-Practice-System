from django.contrib import admin

from apps.exercise.models import Question

# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    '''
    后台管理界面中题目管理的样式
    '''
    list_display = ('qid', 'content', 'usrAns', 'correctAns', 'status', 'user')

admin.site.register(Question, QuestionAdmin)
