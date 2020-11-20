from django.shortcuts import render
from math import isclose

from apps.exercise.models import Question
from apps.account.models import MyUser
from utils.questions_utils import generateProblems, getAns, judgeAns, judgeAns2, isNum
from apps.account.form import LoginForm

# Create your views here.

backup = [''] * 10 # 初始化10个问题都是空
backup_type = [0] * 10 # 0表示填空题，1表示判断题

def index_view(request):
    questions = {}
    '''
      渲染首页
    '''
    Problem = ''
    Your_Ans = ''
    Status = ''
    Correct_Answer = ''
    problem_type = ''
    num_range = ''
    num_cnt = ''
    bracket_decimal = ''
    if request.method == 'POST':
        # 注意返回的是字符串
        problem_type = request.POST.get('problem_type', None)
        num_range = request.POST.get('num_range', None)
        num_cnt = request.POST.get('num_cnt', None)
        bracket_decimal = request.POST.get('bracket_decimal', None)
        # 更新限制条件
            
        if num_range != None:
            if num_range == '':
                num_range = None
            else: 
                _dict = {'0':'10', '1':'100', '2':'1000'}
                num_range = _dict[num_range]
                # 数据范围为[0,num_range]
        if num_cnt != None:
            if num_cnt == '':
                num_cnt = None
            else:
                _dict = {'0':'2', '1':'3', '2':'4', '3':'5'}
                num_cnt = _dict[num_cnt]
                # 运算数个数为num_cnt∈[2,5]
        if bracket_decimal != None:
            if bracket_decimal == '0,1':
                bracket_decimal = '2'
                # ''表示什么都不选 '0'表示选择括号，'1'表示选择小数，'0,1'表示两个都选（改成用'2'）表示
        
        for i in range(10):
            backup_type[i] = problem_type
            backup[i] = generateProblems(problem_type, num_range, num_cnt, bracket_decimal)
            questions[i + 1] = Question(content=backup[i], usrAns='', status='', correctAns='') 
    
    elif request.method == 'GET':
        '''
        获取用户输入的答案，然后传入判题程序，再将判题结果传入Question对象，最后通过模板渲染出来
        '''
        ans = request.GET.getlist('ans', None)
        if ans == []:
            ans = [''] * 10

        for i in range(10):
            ans[i] = ans[i].replace(' ', '') # 去除多余空格
            '''
            backup[i]表示在之前的POST请求中生成的第i个题目的内容
            '''
            if backup[i] == '': # 如果问题为空
                Correct_Answer = ''
                Status = ''
            else: # 计算正确答案并判题
                c_ans = getAns(backup[i], backup_type[i])
                if backup_type[i] == '0': # 填空题
                    Correct_Answer = str(c_ans)
                    if len(Correct_Answer) >= 3 and Correct_Answer[-1] == '0' and Correct_Answer[-2] == '.':
                        Correct_Answer = Correct_Answer[:-2]
                    if isNum(ans[i]): # 保证输入的是数字，如果不合法直接令Status='F'
                        Status = judgeAns(float(ans[i]), c_ans)
                    else:
                        Status = '❌' 
                else: # 判断题的getAns会将等式右边一道左边做差
                    if isclose(c_ans, 0, abs_tol=0.01):
                        Correct_Answer = 'T'
                    else:
                        Correct_Answer = 'F'
                    Status = judgeAns2(ans[i], Correct_Answer)
            
            if backup[i] != '':
                if request.user.is_authenticated:
                    questions[i + 1] = Question.objects.create(content=backup[i], user = request.user, usrAns=ans[i], status=Status, correctAns=Correct_Answer) 
                else:
                    questions[i + 1] = Question.objects.create(content=backup[i], usrAns=ans[i], status=Status, correctAns=Correct_Answer) 
            else:
                questions[i + 1] = Question(content=backup[i], usrAns=ans[i], status=Status, correctAns=Correct_Answer) 
            backup[i] = '' # 每次提交后都需要将其清空
            backup_type[i] = 0
    
    context = {
        'questions': questions,
        'form': LoginForm
    }

    return render(request, 'index.html', context)