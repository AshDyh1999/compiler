# coding=utf-8
import string
import numpy as np

#关键字表
keywards = {'int' : 1, 'float' : 2, 'double' : 3, 'if' : 4, 'else' : 5, 'elseif' : 6, 'while' : 7,
            'return' : 8, 'print' : 9}
#特殊符号表
sp_signls = {'+' : 101, '-' : 102, '*' : 103, '/' : 104, '(' : 105, ')' : 106, '[' : 107,
            ']' : 108, '{' : 109, '}' : 110, ':' : 111, '=' : 112, '>' : 113, '<' : 114, 
            '%' : 115, '&' : 116, '!' : 117 , '|' : 118, '>=' : 119, '<=' : 120, '==' : 121,
            ':=' : 122}
#类别表
classlist = {'keyword' : 100, 'signl' : 200, 'var' : 300, 'const' : 400, 'error' : 500}
#常量表
const_str = 401
constlist = {}
#变量表
var_str = 301
varlist = {}
#全局单词表,扫描结果
signlist = {}
valuelist = {}
# wordlist = []
# 预处理函数，将文件中的空格，换行等无关字符处理掉
def preprocess(file_name):
    try:
        fp_read = open(file_name, 'r')
        fp_write = open('file.txt', 'w')
        flag = 0
        while True:
            read = fp_read.readline()
            if not read:
                break
            length = len(read)
            i = -1
            while i < length - 1:
                i += 1
                if flag == 0:
                    if read[i] == ' ':
                        continue
                if read[i] == '#':
                    break
                elif read[i] == ' ':
                    if flag == 1:
                        continue
                    else:
                        flag = 1
                        fp_write.write(' ')
                elif read[i] == '\t':
                    if flag == 1:
                        continue
                    else:
                        flag = 1
                        fp_write.write(' ')
                elif read[i] == '\n':
                    if flag == 1:
                        continue
                    else:
                        fp_write.write(' ')
                        flag = 1
                else:
                    flag = 2
                    fp_write.write(read[i])
        fp_write.write(' ')#这一步很关键，保证最后一个单词可以被识别
    except Exception as e:
        print(e)

def save(string):
    if string in keywards.keys():
        if string not in signlist.keys():
            valuelist[string] = keywards[string]
            signlist[string] = classlist['keyword']
        # wordlist.append('<'+str(signlist[string])+','+str(valuelist[string])+'>'+string)
    elif string in sp_signls.keys():
        if string not in signlist.keys():
            valuelist[string] = sp_signls[string]
            signlist[string] = classlist['signl']
        # wordlist.append('<'+str(signlist[string])+','+str(valuelist[string])+'>'+string)
    else:
        try:
            float(string)
            save_const(string)
        except ValueError:
            save_var(string)

#两个改变全局(指针)变量的方法
def change_var_str():
    global var_str
    var_str += 1
def change_const_str():
    global const_str
    const_str += 1

#如果某个变量不再符号表中且命名无误则存入符号表，否则标记为错误的变量名
def save_var(string):
    if string not in signlist.keys():
        if len(string.strip()) < 1:
            pass
        else:
            if is_signal(string) == 1:
                signlist[string] = classlist['var']
                valuelist[string] = var_str
                varlist[var_str] = string 
                change_var_str()
                # wordlist.append('<'+str(signlist[string])+','+str(valuelist[string])+'>'+string)
            else:
                signlist[string] = classlist['error']
                valuelist[string] = 500
                # wordlist.append('<'+str(signlist[string])+','+str(valuelist[string])+'>'+string)
                

#如果某个常量不在符号表中，将其存入符号表
def save_const(string):
    if string not in signlist.keys():
        signlist[string] = classlist['const']
        valuelist[string] = const_str
        constlist[const_str] = string
        change_const_str()
    # wordlist.append('<'+str(signlist[string])+','+str(valuelist[string])+'>'+string)

#检测是否是一个合格的变量名，以下划线'_'或者'字母开头'
def is_signal(s):
    if s[0] == '_' or s[0] in string.ascii_letters:
        for i in s:
            if i in string.ascii_letters or i == '_' or i in string.digits:
                pass
            else:
                return 0
        return 1
    else:
        return 0

#识别函数，用来识别判定一个token的类型
def recognition(filename):
    try:
        fp_read = open(filename, 'r')
        string = ""
        flag = 0
        while True:
            read = fp_read.read(1)
            if not read:
                break
            if read == ' ':
                if len(string.strip()) < 1:
                    flag = 0
                    pass
                else:
                    save(string)
                    string = ""
                    flag = 0
            elif read == '(':
                save(string)
                string = ""
                save('(')
                flag = 0
            elif read == ')':
                save(string)
                string = ""
                save(')')
                flag = 0
            elif read == '[':
                save(string)
                string = ""
                save('[')
                flag = 0
            elif read == ']':
                save(string)
                string = ""
                save(']')
                flag = 0
            elif read == '{':                
                save(string)
                string = ""
                save('{')
                flag = 0
            elif read == '}':
                save(string)
                string = ""
                save('}')
                flag = 0
            elif read == '|':                
                save(string)
                string = ""
                save('|')
                flag = 0
            elif read == '+':
                save(string)
                string = ""
                save('+')
                flag = 0
            elif read == '-':
                save(string)
                string = ""
                save('-')
                flag = 0
            elif read == '*':
                save(string)
                string = ""
                save('*')
                flag = 0
            elif read == '/':
                save(string)
                string = ""
                save('/')
                flag = 0
            elif read == '<':            
                save(string)
                flag = 1
                string = ""
                string += read
                continue
            elif read == '>':
                save(string)
                flag = 1
                string = ""
                string += read
                continue
            elif read == ':':
                save(string)
                flag = 1
                string = ""
                string += read
                continue
            elif read == '=':
                if flag == 1:
                    string += read
                    save(string)
                    string = ""
                    flag = 0
                else:
                    flag = 1
                    string += read
                    continue
            else:
                string += read

    except Exception as e:
        print(e)

def main():
    preprocess('test2.txt')
    recognition('file.txt')
    filewrite = open('result.txt', 'w')
    print("属性字：")
    for i in signlist.keys():
        st = "<"+str(signlist[i])+","+str(valuelist[i])+">"+str(i)+"\n"
        print( "<", signlist[i], ",", valuelist[i], ">", i)
        filewrite.write(st)
    filewrite.close()
    np.save('varlist.npy', varlist) 
    np.save('constlist.npy',constlist)
    # filewrite2 = open('单词串.txt', 'w')
    # filewrite2.write(str(wordlist))
    # filewrite2.close()
    # filewrite3 = open('result_constlist.txt', 'w')
    # filewrite3.write(str(const_str))
    # filewrite3.close()
    print("常量表：",constlist)
    print("变量表：",varlist)
    # print("单词串：",wordlist)
if __name__ == '__main__':
    main()