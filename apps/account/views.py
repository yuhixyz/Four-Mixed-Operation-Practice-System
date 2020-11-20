from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages

from django.contrib.auth.hashers import make_password # 用于生成哈希后的密码
from apps.account.form import LoginForm
from apps.exercise.models import Question

from django.template.defaulttags import register

# Create your views here.


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
            else:
                messages.error(request, '登录失败') # 暂时没用到
    return HttpResponseRedirect(reverse('home')) # 返回首页

def logout_view(request):
    logout(request) # 注销
    # print(make_password("Q18010130")) # 用于生成哈希后的密码
    return HttpResponseRedirect(reverse('home')) # 返回首页

def history_view(request):
    # 从所有题目中过滤出当前用户做的题，加入到questions列表中，通过前端模板渲染出来
    questions = []
    questions_dir = {} # {key, value} = {updated_at, questions_list} 按照每次测试10个一组
    all_ac_rate = {} # {key, value} = {updated_at, ac_rate} 
    if request.user.is_authenticated:
        questions = Question.objects.filter(user=request.user).order_by('-updated_at') # 按照最近的时间排序
        ac_questions = questions.filter(status='✔️')
        questions_list = []
        cnt = 0
        for question in questions:
            if cnt == 9:
                questions_list.append(question)
                questions_dir[question.updated_at] = questions_list
                ac_cnt = 0
                for q in questions_list:
                    if q.status == '✔️':
                        ac_cnt += 1
                all_ac_rate[questions_list[0].updated_at] = ac_cnt / 10 * 100
                questions_list = []
                cnt = 0
            else:
                questions_list.append(question)
                cnt += 1
        up = len(ac_questions)
        down = len(questions)
        request.user.ac_rate = round(up / down * 100 if down else 100, 2)

    context = {
        'form': LoginForm,
        'questions_dir': questions_dir,
        'all_ac_rate': all_ac_rate
    }
    if request.method == 'GET':
        return render(request, 'history.html', context)
