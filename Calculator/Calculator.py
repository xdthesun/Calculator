# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-01-25 14:26
# @Author  : zhanghui31
# @FileName: Calculator.py

import re


class Calculator(object):

    def __init__(self):
        # 设置运算符优先级
        self.Operator={
                       '(':4,
                       ')':3,
                       '*':2,
                       '/':2,
                       '+':1,
                       '-':1,
                       '.':0}
    def operate(self, operandA, operandB, operator):
        if operator == '+':
            return operandA + operandB
        elif operator == '-':
            return operandA - operandB
        elif operator == '*':
            return operandA * operandB
        elif operator == '/':
            return operandA/operandB
        else:
            print("运算符有误，请确认！")
            return None

    def isFormula(self, str):
        temp = []
        strs = str.replace(' ', '')
        for i in strs:
            if i is '(':
                temp.append(i)
            elif i is ')':
                if len(temp) == 0:
                    return False
                elif temp[-1] is '(':
                    temp.pop()
                else:
                    temp.append(i)
        pattern = r'^\(*\d+(\.\d+)?((\+|\*|/|-)\(*\d+(\.\d+)?\)*)*(\+|\*|/|-)\d+(\.\d+)?\)*$'
        res = re.match(pattern, strs)
        if len(temp) == 0 and res is not None and res.endpos == len(strs):
            return True
        return False

    def Infix2Prefix(self, infixstrs):
        """
            1.初始化两个栈:运算符栈s1，储存中间结果的栈s2
            2.从右至左扫描中缀表达式
            3.遇到操作数时，将其压入s2
            4.遇到运算符时，比较其与s1栈顶运算符的优先级
                4.1如果s1为空，或栈顶运算符为右括号“)”，则直接将此运算符入栈
                4.2否则，若优先级比栈顶运算符的较高或相等，也将运算符压入s1
                4.3否则，将s1栈顶的运算符弹出并压入到s2中，再次转到(4-1)与s1中新的栈顶运算符相比较
            5.遇到括号时
                5.1如果是右括号“)”，则直接压入s1
                5.2如果是左括号“(”，则依次弹出S1栈顶的运算符，并压入S2，直到遇到右括号为止，此时将这一对括号丢弃
            6.重复步骤2至5，直到表达式的最左边
            7.将s1中剩余的运算符依次弹出并压入s2
            8.依次弹出s2中的元素并输出，结果即为中缀表达式对应的前缀表达式
        :param strs: 中缀式字符串
        :return: 转换后的前缀式
        """
        infixstrs = infixstrs.replace(' ','')
        stack1 = []
        stack2 = []
        if self.isFormula(infixstrs) is not True:
            raise Exception("请输入正确格式的算式！！！")
        infixstrs = infixstrs.replace(' ', '')
        intflag = 0
        decimalflag = 0
        strs = infixstrs[::-1]
        for i in strs:
            if i.isdigit() or self.Operator[i] == 0:
                if i.isdigit() is False and self.Operator[i] == 0:
                    decpart = stack2.pop()
                    for j in range(intflag):
                       decpart = decpart/10
                    stack2.append(decpart)
                    decimalflag = 1
                    intflag = 0
                else:
                    if intflag == 0 and decimalflag == 0:
                        stack2.append(int(i))
                    elif intflag == 0 and decimalflag == 1:
                        stack2.append(stack2.pop() + int(i))
                    elif intflag > 0 :
                        dec = 1
                        for j in range(intflag):
                            dec = 10 * dec
                        stack2.append(stack2.pop() + int(i) * dec)
                    intflag = intflag + 1
            else:
                intflag = 0
                decimalflag = 0
                if len(stack1) == 0  or self.Operator[i] == 3:
                    stack1.append(i)
                elif self.Operator[i] == 4:
                    length = len(stack1)
                    for j in range(length):
                        temp = stack1.pop()
                        if self.Operator[temp] == 3:
                            break
                        stack2.append(temp)
                elif self.Operator[i] == 1 or self.Operator[i] == 2:
                    if self.Operator[stack1[-1]] == 3:
                        stack1.append(i)
                    elif self.Operator[stack1[-1]] <= self.Operator[i] :
                        length = len(stack1)
                        for j in range(length):
                            if len(stack1) == 0 or self.Operator[stack1[-1]] > self.Operator[i]:
                                break
                            temp = stack1.pop()
                            stack2.append(temp)
                        stack1.append(i)
                    else:
                        stack1.append(i)
        while len(stack1)>0:
            stack2.append(stack1.pop())
        result = stack2
        result.reverse()
        return result

    def Infix2Suffix(self, infixstrs):
        """
            1.初始化两个栈：运算符栈s1和储存中间结果的栈s2；
            2.从左至右扫描中缀表达式；
            3.遇到操作数时，将其压s2；
            4.遇到运算符时，比较其与s1栈顶运算符的优先级：
                4.1如果s1为空，或栈顶运算符为左括号“(”，则直接将此运算符入栈；
                4.2否则，若优先级比栈顶运算符的高，也将运算符压入s1（注意转换为前缀表达式时是优先级较高或相同，而这里则不包括相同的情况）；
                4.3否则，将s1栈顶的运算符弹出并压入到s2中，再次转到(4-1)与s1中新的栈顶运算符相比较；
            5遇到括号时：
                5.1如果是左括号“(”，则直接压入s1；
                5.2如果是右括号“)”，则依次弹出s1栈顶的运算符，并压入s2，直到遇到左括号为止，此时将这一对括号丢弃；
                5.3重复步骤2至5，直到表达式的最右边；
            6.将s1中剩余的运算符依次弹出并压入s2；
            7.依次弹出s2中的元素并输出，结果的逆序即为中缀表达式对应的后缀表达式
        :param infixstrs: 中缀式算式
        :return: 转换后的后缀式
        """
        infixstrs = infixstrs.replace(' ', '')
        stack1 = []
        stack2 = []
        if self.isFormula(infixstrs) is False:
            raise Exception("请输入正确格式的算式！！！")
        # 用来标识是否是连续的数字或者小数点
        intflag = 0
        decimalflag = 0
        for i in infixstrs:
            if i.isdigit() or self.Operator[i] == 0:
                if i.isdigit() is False and self.Operator[i] == 0:
                    intflag = 0
                    decimalflag = 1
                elif intflag == 0:
                    stack2.append(int(i))
                elif decimalflag == 0 and intflag > 0:
                    stack2.append(stack2.pop()*10 + int(i))
                elif decimalflag == 1 and intflag > 0:
                    prepart = stack2.pop()
                    endpart = int(i)
                    for j in range(intflag):
                        endpart = endpart/10
                    stack2.append(prepart + endpart)
                intflag = intflag + 1

            else:
                intflag = 0
                decimalflag = 0
                if len(stack1) == 0 or self.Operator[i] == 4:
                    stack1.append(i)
                elif self.Operator[i] == 3:
                    length = len(stack1)
                    for j in range(length):
                        temp = stack1.pop()
                        if self.Operator[temp] == 4:
                            break
                        stack2.append(temp)

                elif self.Operator[i] == 1 or self.Operator[i] == 2:
                    if self.Operator[stack1[-1]] == 4:
                        stack1.append(i)
                    elif self.Operator[stack1[-1]] >= self.Operator[i]:
                        length = len(stack1)
                        for j in range(length):
                            if len(stack1) == 0 or self.Operator[stack1[-1]] < self.Operator[i]:
                                break
                            temp = stack1.pop()
                            stack2.append(temp)
                        stack1.append(i)
                    else:
                        stack1.append(i)
        while len(stack1)>0:
            stack2.append(stack1.pop())
        result = stack2
        return result

    def calculate(self, strs, is_Prefix=True):
        """
            根据转换后的式子计算最终的结果
        :param strs:
        :param is_Suffix: 是否是后缀式
        :return:
        """

        result = []
        if is_Prefix:
            strs = strs[::-1]
        for i in strs :
            if i in self.Operator.keys():
                operandA = result.pop()
                operandB = result.pop()
                if is_Prefix:
                    calres = self.operate(operandA, operandB, i)
                else:
                    calres = self.operate(operandB, operandA, i)
                result.append(calres)
            else:
                result.append(i)
        return result[0]


if __name__ == '__main__':
    # print(Calculator().isFormula("123*(12/2)"))
    # print(Calculator().isFormula("(2+22 + (33+2+23312+(213+3123)+2)-1)"))
    test = Calculator()
    print(test.Infix2Prefix("1+((32.34+3)*4)-5"))
    # print(test.Infix2Suffix("1+((32.34+3)*4)-5"))
    # print(test.Infix2Suffix("32.34+3"))

    print("%.2f"% test.calculate(test.Infix2Suffix("1+((32.34+3)*4)-5"), is_Prefix=False))
    print("%.2f"% test.calculate(test.Infix2Prefix("1+((32.349+3)*4)-5")))
    # print(test.calculate(['-', '*', '+', 3, 4, 5, 6]))
    pass

