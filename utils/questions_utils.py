import random

from math import isclose

def isNum(x : str) -> bool :
    '''
        判断x是否为合法的整数或者小数
        合法返回 True
    '''
    if x == '':
        return False
    if x[0] == '-':
        x = x[1:] # 将第一个负号略去再判断
        if x == '':
            return False
    if '.' in x: # 判断x是否为小数（小数点只有1个，且小数点前后都有数字）
        dot_cnt = 0
        for y in x:
            if y == '.':
                dot_cnt += 1
        if dot_cnt > 1:
            return False
        pos = x.find('.');
        if pos == 0 or pos == len(x):
            return False
        for i in range(0, pos):
            if x[i] < '0' or x[i] > '9' or (i and x[i] == '-'):
                return False
        for i in range(pos + 1, len(x)):
            if x[i] < '0' or x[i] > '9':
                return False
        return True
    else: # 判断x是否为整数
        return x.isdigit()
    

def generateProblems(problem_type : str, num_range : str, num_cnt : str, bracket_decimal: str) -> str :
    '''
        根据参数条件生成运算式
        数据范围为[0,num_range]
        运算数个数为num_cnt∈[2,5]
        bracket_decimal为 '0'表示选择括号，'1'表示选择小数，'0,1'表示两个都选（改成用'2'）表示
    '''
    operator = ['+', '-', '*', '/']
    if problem_type == None or num_range == None or num_cnt == None \
        or bracket_decimal == None:
        return ''
    problem = []
    # if problem_type == '0': # 填空题
    # if bracket_decimal == '' or bracket_decimal == '0': # 没有小数
    num_list = []
    operator_list = []
    cnt = int(num_cnt)
    rg = int(num_range)
    for i in range(cnt):
        if bracket_decimal == '' or bracket_decimal == '0':
            num_list.append(random.randint(1, rg))
        else: # 小数
            num_list.append(round(random.uniform(0, rg), 2))
    for i in range(cnt - 1):
        operator_list.append(operator[random.randint(0, 3)])
    # print(num_list)
    # print(operator_list)
    for i in range(cnt):
        problem.append(str(num_list[i]))
        if i != cnt - 1:
            problem.append(operator_list[i])
    if bracket_decimal == '0' or bracket_decimal == '2': # 需要加括号
        if cnt > 2: # 只有大于两个数字才加括号
            # 先插左括号
            temp = [0, 2, 4, 6, 8]
            pos = random.randint(0, cnt - 2) # 左括号插入到第pos个位置的前面
            pos = temp[pos]
            problem = problem[:pos] + ['('] + problem[pos:]
            # 插右括号，右括号与左括号之前至少有两个数字
            # 右括号插入位置：pos+3 / post+5 / pos+7 ...
            temp = [pos + 3, pos + 5, pos + 7]
            pos = temp[random.randint(0, cnt - 3)] # 需要插到pos的后面
            problem = problem[ : pos + 1] + [')'] + problem[pos + 1: ]
                
    problem.append('=')

    if problem_type == '1': # 如果是判断题
        tmp_problem_str = ' '.join(problem) # 判断题的等式左边
        t = random.randint(0, 3)
        if t == 0 or t == 2:
            tmp = str(round(getAns(tmp_problem_str, '0'), 2))
        elif t == 1:
            tmp = str(round(getAns(tmp_problem_str, '0') - 1, 2))
        else:
            tmp = str(round(getAns(tmp_problem_str, '0') + 1, 2))

        if len(tmp) >= 3 and tmp[-1] == '0' and tmp[-2] == '.':
            tmp = tmp[:-2]
        problem.append(tmp)

    problem_str = ' '.join(problem) # 将列表转化为字符串
    return problem_str



def getValue(operator : str, op1 : float, op2 : float) -> float :
    '''
        对操作数op1和op2进行operator运算
    '''
    if operator == '+':
        return op1 + op2
    elif operator == '-':
        return op1 - op2
    elif operator == '*':
        return op1 * op2
    elif operator == '/':
        return op1 / op2

def getAns(infix_expression : str, problem_type : str) -> float :
    '''
        中缀表达式求值
        参数：空格分割的中缀表达式
    '''
    token_list = infix_expression.split()
    if problem_type == '0' and len(token_list) > 0 and token_list[-1] == '=':
        token_list.pop() # 去掉最后的'='
    elif problem_type == '1' and len(token_list) >= 3:
        tmp = token_list[-1]
        token_list = token_list[:-2]
        token_list.append('-')
        token_list.append(tmp)

    # print(token_list)
    # 运算符优先级字典
    pre_dict = {'*':3,'/':3,'+':2,'-':2,'(':1}
    # 运算符栈
    operator_stack = []
    # 操作数栈
    operand_stack = []
    for token in token_list:
        # 左括号进运算符栈
        if token == '(':
            operator_stack.append(token)
        # 碰到右括号，就要把栈顶的左括号上面的运算符都弹出求值
        elif token == ')':
            top = operator_stack.pop()
            while top != '(':
                # 每弹出一个运算符，就要弹出两个操作数来求值
                # 注意弹出操作数的顺序是反着的，先弹出的数是op2
                op2 = operand_stack.pop()
                op1 = operand_stack.pop()
                # 求出的值要压回操作数栈
                # 这里用到的函数getValue在下面有定义
                operand_stack.append(getValue(top,op1,op2))
                # 弹出下一个栈顶运算符
                top = operator_stack.pop()
        # 碰到运算符，就要把栈顶优先级不低于它的都弹出求值
        elif token in '+-*/':
            while operator_stack and pre_dict[operator_stack[-1]] >= pre_dict[token]:
                top = operator_stack.pop() # 栈顶优先级大于当前运算符，需要先计算栈顶的运算
                op2 = operand_stack.pop() # 取出两个数，作栈顶的运算，然后重新压入操作栈
                op1 = operand_stack.pop()
                operand_stack.append(getValue(top,op1,op2))
            # 别忘了最后让当前运算符进栈
            operator_stack.append(token)
        # 数字进操作数栈
        else:
            operand_stack.append(float(token))
    # 表达式遍历完成后，栈里剩下的操作符也都要求值   
    while operator_stack:
        top = operator_stack.pop()
        op2 = operand_stack.pop()
        op1 = operand_stack.pop()
        operand_stack.append(getValue(top,op1,op2))
    # 最后栈里只剩下一个数字，这个数字就是整个表达式最终的结果
    return operand_stack[0]

def judgeAns(usrAns: float, correctAns : float) -> str:
    '''
        填空题以两个浮点数判断用户答案和正确答案的一致性
        正确返回'✔️'
        错误返回'❌'
    '''
    # 若答案小数点后超过2位，自动四舍五入到小数点后2位
    # 保证正确性，保证答案偏差不超过0.01，且两个值四舍五入后的值偏差不能超过0.01
    return '✔️' if isclose(usrAns, correctAns, abs_tol=0.01) and (round(usrAns, 2) - round(correctAns, 2) < 0.001) else '❌'

def judgeAns2(usrAns: str, correctAns : str) -> str:
    '''
        判断题的判定
    '''
    return '✔️' if usrAns == correctAns else '❌'