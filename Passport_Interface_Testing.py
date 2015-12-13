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
                    info = {'appid': row['appid'], 'username': row['username'], 'password': row['password'], 'repassword': row['repassword']} #csv里的每一行测试实例
                    data = urllib.parse.urlencode(info).encode(encoding='UTF8')         #将信息编码成urllib能够识别的类型,注意的是python2.7用的ASCII编码,python3.X要UTF8转码  
                    req = urllib.request.Request(test_register.url, data)               #构造请求对象  
                    response = urllib.request.urlopen(req)                              #执行post请求
                    response_dict = eval(response.read())                               #读取发回的数据,并将字符串转换为字典 
                    self.assertEqual(response_dict["res"], eval(row['res']))            #用户名注册模块---您看到此信息,代表当行测试数据未通过---   


'''
unittest.main(),固定格式,用于默认调用unittest模块
'''
if __name__ == '__main__':
    unittest.main()
