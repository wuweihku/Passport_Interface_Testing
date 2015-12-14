# -*- coding: utf-8 -*-
import unittest                                                                         #支持Python单元测试模块
import urllib.parse                                                                     #这里urllib.parse要精确到子模块,否则会报错
import urllib.request                                                                   #这里urllib.request要精确到子模块,否则会报错
import csv                                                                              #支持csv自动化导表

'''
一个子功能模块对应一个测试类
'''

#对应模块:用户名注册
class test_register(unittest.TestCase):
    url = 'http://passportapi.15166.com/user/signup'                                    #所要访问的url,一个测试类对应一个url
    
    def setUp(self):                                                                    #文件/数据库/网络服务初始化工作
        pass

    def tearDown(self):                                                                 #销毁工作
        pass

    def test_register_cases(self):                                                      #执行测试功能的函数
        with open('register_data.csv') as csvfile:                                      #打开csv文件流
            reader = csv.DictReader(csvfile)                                            #创建文件流对象
            register_num=0                                                              #计算一共跑了多少条测试数据
            for row in reader:                                                          #这里的row对应csv表里的一行数据,第一行数据自动作为字段名,第二行数据开始作为测试实例
                register_num+=1                                                         
                with self.subTest(row=row):                                             #row=i,会报错row is not defined,必须用row=row(这里用的是subTest功能)
                    print("正在为'用户名注册模块'执行第 %d 条测试数据"%register_num)                                              #每跑一条数据,显示一次当前进度
                    info = {'appid': row['appid'], 'username': row['username'], 'password': row['password'], 'repassword': row['repassword']} #csv里的每一行测试实例，这里不用过滤空值，空值可以作为测试用例，引发异常
                    data = urllib.parse.urlencode(info).encode(encoding='UTF8')         #将信息编码成urllib能够识别的类型,注意的是python2.7用的ASCII编码,python3.X要UTF8转码  
                    req = urllib.request.Request(test_register.url, data)               #构造请求对象  
                    response = urllib.request.urlopen(req)                              #执行post请求
                    response_dict = eval(response.read())                               #读取发回的数据,并将字符串转换为字典 
                    self.assertEqual(response_dict["res"], eval(row['res']))            #用户名注册模块---您看到此信息,代表当行测试数据未通过---   

#对应模块:登录、快速登录
class test_login(unittest.TestCase):
    url = 'http://passportapi.15166.com/user/login'

    def setUp(self):  
        pass
    
    def tearDown(self):
        pass

    def test_login_cases(self): 
        with open('login_data.csv') as csvfile:
            reader = csv.DictReader(csvfile) 
            login_num=0
            for row in reader: 
                login_num+=1 
                with self.subTest(row=row): 
                    print("正在为'登录、快速登录模块'执行第 %d 条测试数据"%login_num) 
                    
                    #留空就判不合法了，不需要的参数我是直接当成不传的--邓棚云
                    #sessionid可以为空
                    #guid可以为空
                    #username、mail、phone三者不能同时为空
                    #实际情况是，机会会字典限制你传递的值，你根本没机会同时传手机+用户名+邮箱过去，因为有优先级判断，也有填数据的入口限制
                    #所以在这里读取字典的时候，就要过滤空值了
                
                    info = {'appid': row['appid'], 'username': row['username'], 'mail': row['mail'], 'phone': row['phone'],'password': row['password'],'guid': row['guid'],'sessionid': row['sessionid']}
                    list_del = []                                                       #定义一个用来存储空值键的列表
                    for k in info.keys():
                        if info[k] =='':                                                #判断对应键的值为空时，将该键加入list_del待删除
                            list_del.append(k)
                    for i in list_del:                                                  #一一删除存储在list_del中的空值键
                        del info[i] 

                    data = urllib.parse.urlencode(info).encode(encoding='UTF8')
                    req = urllib.request.Request(test_login.url, data) 
                    response = urllib.request.urlopen(req) 
                    response_dict = eval(response.read())
                    self.assertEqual(response_dict["res"], eval(row['res']))            #登录、快速登录模块---您看到此信息,代表当行测试数据未通过---    
                 
'''
unittest.main(),固定格式,用于默认调用unittest模块
'''
if __name__ == '__main__':
    unittest.main()
