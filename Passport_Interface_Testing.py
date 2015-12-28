# -*- coding: utf-8 -*-
import unittest                                                                             #支持Python单元测试模块
import urllib.parse                                                                         #这里urllib.parse要精确到子模块,否则会报错
import urllib.request                                                                       #这里urllib.request要精确到子模块,否则会报错
import csv                                                                                  #支持csv自动化导表
import sys                                                                                  #用来打log


'''
一个子功能模块对应一个测试类,此版本将输出信息存储于log文件夹下的log文件之中，再将当次的log文件print到屏幕上，方便查看信息
'''

#对应模块:2.1用户名注册
class test_signup(unittest.TestCase):
    url = 'http://passportapi.15166.com/user/signup'                                        #所要访问的url,一个测试类对应一个url
    
    def setUp(self):                                                                        #文件/数据库/网络服务初始化工作
        pass

    def tearDown(self):                                                                     #销毁工作
        pass

    def test_signup_cases(self):                                                            #执行测试功能的函数
        with open('csv/signup_data.csv') as csvfile:                                            #打开csv文件流
            reader = csv.DictReader(csvfile)                                                #创建文件流对象
            signup_num=0                                                                    #计算一共跑了多少条测试数据
            for row in reader:                                                              #这里的row对应csv表里的一行数据,第一行数据自动作为字段名,第二行数据开始作为测试实例
                signup_num+=1                                                         
                with self.subTest(row=row):                                                 #row=i,会报错row is not defined,必须用row=row(这里用的是subTest功能)
                    print("正在为'用户名注册模块'执行第 %d 条测试数据"%signup_num)                                              #每跑一条数据,显示一次当前进度
                    info = {'appid': row['appid'], 'username': row['username'], 'password': row['password'], 'repassword': row['repassword']} #csv里的每一行测试实例，这里不用过滤空值，空值可以作为测试用例，引发异常
                    data = urllib.parse.urlencode(info).encode(encoding='UTF8')             #将信息编码成urllib能够识别的类型,注意的是python2.7用的ASCII编码,python3.X要UTF8转码  
                    req = urllib.request.Request(test_signup.url, data)                     #构造请求对象  
                    response = urllib.request.urlopen(req)                                  #执行post请求
                    response_dict = eval(response.read())                                   #读取发回的数据,并将字符串转换为字典 
                    self.assertEqual(response_dict["res"], eval(row['res']))    #用户名注册模块---您看到此信息,代表当行测试数据未通过---  
                 
        print("----------------------------------------------------------------------------------------------------------------------")
#对应模块:2.2登录及快速登录
class test_login(unittest.TestCase):
    url = 'http://passportapi.15166.com/user/login'

    def setUp(self):  
        pass
    
    def tearDown(self):
        pass

    def test_login_cases(self): 
        with open('csv/login_data.csv') as csvfile:
            reader = csv.DictReader(csvfile) 
            login_num=0
            for row in reader: 
                login_num+=1 
                with self.subTest(row=row): 
                    print("正在为'登录及快速登录模块'执行第 %d 条测试数据"%login_num) 
                    
                    #留空就判不合法了，不需要的参数我是直接当成不传的--邓棚云
                    #sessionid可以为空
                    #guid可以为空
                    #username、mail、phone三者不能同时为空
                    #实际情况是，机会会字典限制你传递的值，你根本没机会同时传手机+用户名+邮箱过去，因为有优先级判断，也有填数据的入口限制
                    #所以在这里读取字典的时候，就要过滤空值了
                
                    info = {'appid': row['appid'], 'username': row['username'], 'mail': row['mail'], 'phone': row['phone'],'password': row['password'],'guid': row['guid'],'sessionid': row['sessionid']}
                    list_del = []                                                           #定义一个用来存储空值键的列表
                    for k in info.keys():
                        if info[k] =='':                                                    #判断对应键的值为空时，将该键加入list_del待删除
                            list_del.append(k)
                    for i in list_del:                                                      #一一删除存储在list_del中的空值键
                        del info[i] 

                    data = urllib.parse.urlencode(info).encode(encoding='UTF8')
                    req = urllib.request.Request(test_login.url, data) 
                    response = urllib.request.urlopen(req) 
                    response_dict = eval(response.read())
                    self.assertEqual(response_dict["res"], eval(row['res']))    #登录、快速登录模块---您看到此信息,代表当行测试数据未通过---    
        print("----------------------------------------------------------------------------------------------------------------------")

#对应模块:2.3获取绑定手机
class test_findbindphone(unittest.TestCase):
    url = 'http://passportapi.15166.com/user/findbindphone'

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_findbindphone_cases(self):
        with open('csv/findbindphone_data.csv') as csvfile:
            reader = csv.DictReader(csvfile) 
            findbindphone_num=0
            for row in reader: 
                findbindphone_num+=1
                with self.subTest(row=row):
                    print("正在为'获取绑定手机模块'执行第 %d 条测试数据"%findbindphone_num)
                    #这里应该是不需要进行空值过滤的，因为appid不可能为空，另外username空值可以作为正常的测试用例，不会影响后续测试流程
                    info = {'appid': row['appid'], 'username': row['username']}
                    data = urllib.parse.urlencode(info).encode(encoding='UTF8')
                    req = urllib.request.Request(test_findbindphone.url, data)
                    response = urllib.request.urlopen(req)
                    response_dict = eval(response.read())
                    self.assertEqual(response_dict["res"], eval(row['res']))    #获取绑定手机模块---您看到此信息,代表当行测试数据未通过---                        
        print("----------------------------------------------------------------------------------------------------------------------")

#对应模块:2.4获取验证码
class test_getcode(unittest.TestCase):
    url = 'http://passportapi.15166.com/user/getcode'

    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_getcode_cases(self):
        with open('csv/getcode_data.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            getcode_num=0
            for row in reader:
                getcode_num+=1
                with self.subTest(row=row):
                    print("正在为'获取验证码模块'执行第 %d 条测试数据"%getcode_num)
                    #这里username可以为空，guid可以为空，但是二者不能同时为空
                    #我这里没有做空值筛选，看情况是可以进行测试的，不会有影响。如果遇到了问题，再在此处补一个空值筛选的流程。
    
                    info = {'appid': row['appid'], 'username': row['username'], 'phone': row['phone'],'code_type': row['code_type'],'guid': row['guid']}
                    data = urllib.parse.urlencode(info).encode(encoding='UTF8')
                    req = urllib.request.Request(test_getcode.url, data)
                    response = urllib.request.urlopen(req)
                    response_dict = eval(response.read())
                   
                    # 下面的代码用于显示一个5分钟有效期的code_id，以方便2.5/2.6模块
                    # print(response_dict["code_id"]+"用于显示一个5分钟有效期的code_id,以方便2.5/2.6模块进行测试")
                    # print(response_dict)
                    self.assertEqual(response_dict["res"], eval(row['res']))    #获取验证码模块---您看到此信息,代表当行测试数据未通过---
        print("----------------------------------------------------------------------------------------------------------------------")
                    
#对应模块:2.5找回密码
class test_changepwdbycode(unittest.TestCase):
    url = 'http://passportapi.15166.com/user/changepwdbycode'
    
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_changepwdbycode_cases(self):
        with open('csv/changepwdbycode_data.csv') as csvfile:
            reader = csv.DictReader(csvfile) 
            changepwdbycode_num=0
            for row in reader:
                changepwdbycode_num+=1
                with self.subTest(row=row):
                    print("正在为'找回密码模块'执行第 %d 条测试数据"%changepwdbycode_num)
                    #这里的code_id是32位字符串，必须由2.4取验证码的返回消息中获得，5分钟有效期
                    #那我就每次测这个模块的时候，经2.4正确地获得一个code_id拿来用
                    #由于要测试code_id正确，错误，空的情况，因此还是得自己填写表
                    #若测试此部分时，返回10011，说明code_id过期了，请重新获取一个5分钟有效期的码，填入相应的表中                    
                    
                    #向研发那边提个需求，让他们给一个超级账号，sessionid与code_id不受时间限制                    

                    info = {'appid': row['appid'],'code_id' : row['code_id'], 'username': row['username'], 'phone': row['phone'],'password': row['password']}
                    data = urllib.parse.urlencode(info).encode(encoding='UTF8')
                    req = urllib.request.Request(test_changepwdbycode.url, data)  
                    response = urllib.request.urlopen(req)
                    response_dict = eval(response.read())
                    self.assertEqual(response_dict["res"], eval(row['res']))    #找回密码模块---您看到此信息,代表当行测试数据未通过---
        print("----------------------------------------------------------------------------------------------------------------------")
            
#对应模块:2.6绑定手机
class test_bindphone(unittest.TestCase):
    url = 'http://passportapi.15166.com/user/bindphone'

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_bindphone_cases(self):
        with open('csv/bindphone_data.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            bindphone_num=0 
            for row in reader:
                bindphone_num+=1
                with self.subTest(row=row):
                    print("正在为'绑定手机模块'执行第 %d 条测试数据"%bindphone_num)
                    #向研发那边提个需求，让他们给一个超级账号，sessionid与code_id不受时间限制 
                    
                    info = {'appid': row['appid'],'code_id' : row['code_id'], 'username': row['username'], 'guid' : row['guid'], 'phone': row['phone'],'password': row['password']}
                    data = urllib.parse.urlencode(info).encode(encoding='UTF8')
                    req = urllib.request.Request(test_bindphone.url, data)
                    response = urllib.request.urlopen(req)
                    response_dict = eval(response.read())
                    self.assertEqual(response_dict["res"], eval(row['res']))    #绑定手机模块---您看到此信息,代表当行测试数据未通过---
        print("----------------------------------------------------------------------------------------------------------------------")

#对应模块:2.7修改信息
class test_editinfo(unittest.TestCase):
    url = 'http://passportapi.15166.com/user/editinfo'
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_editinfo_cases(self):
        with open('csv/editinfo_data.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            editinfo_num=0
            for row in reader:
                editinfo_num+=1
                with self.subTest(row=row):
                    print("正在为'修改信息模块'执行第 %d 条测试数据"%editinfo_num)
                    
                    info = {'appid': row['appid'], 'username': row['username'], 'nickname': row['nickname'],'postcode': row['postcode'],'address': row['address'],'gender': row['gender'],'province': row['province'],'job': row['job'],'income': row['income'],'education': row['education'],'industry': row['industry']}                    
                    data = urllib.parse.urlencode(info).encode(encoding='UTF8')
                    req = urllib.request.Request(test_editinfo.url, data)
                    response = urllib.request.urlopen(req)
                    response_dict = eval(response.read())
                    self.assertEqual(response_dict["res"], eval(row['res']))    #修改信息模块---您看到此信息,代表当行测试数据未通过---
        print("----------------------------------------------------------------------------------------------------------------------")

#对应模块:2.8完善用户名
class test_addusername(unittest.TestCase):
    url = 'http://passportapi.15166.com/user/addusername'

    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_addusername_cases(self):
        with open('csv/addusername_data.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            addusername_num=0
            for row in reader:
                addusername_num+=1
                with self.subTest(row=row):
                    print("正在为'完善用户名模块'执行第 %d 条测试数据"%addusername_num)
                    info = {'appid': row['appid'], 'username': row['username'], 'guid': row['guid'],'password': row['password'],'phone': row['phone']}
                    data = urllib.parse.urlencode(info).encode(encoding='UTF8')
                    req = urllib.request.Request(test_addusername.url, data)
                    response = urllib.request.urlopen(req)
                    response_dict = eval(response.read())
                    self.assertEqual(response_dict["res"], eval(row['res']))    #完善用户名模块---您看到此信息,代表当行测试数据未通过---
        print("----------------------------------------------------------------------------------------------------------------------")
                    
                 
'''
unittest.main(),固定格式,用于默认调用unittest模块
'''
import time

if __name__ == '__main__':
    log_file = 'log/log_%s.txt'%time.strftime("%Y_%m_%d_%H:%M:%S", time.localtime()) #定义log路径及文件名
    f = open(log_file, "w")
    runner = unittest.TextTestRunner(f)
    unittest.main(testRunner=runner)
    f.close()
