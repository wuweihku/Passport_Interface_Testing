# -*- coding: utf-8 -*-
import unittest                                                                             #支持Python单元测试模块
import urllib.parse                                                                         #这里urllib.parse要精确到子模块,否则会报错
import urllib.request                                                                       #这里urllib.request要精确到子模块,否则会报错
import csv                                                                                  #支持csv自动化导表
import sys                                                                                  #用来打log
import hashlib                                                                              #支持MD5加密
import json                                                                                 #支持json
import time                                                                                 #支持时间

'''
一个子功能模块对应一个测试类,此版本将输出信息存储于log文件夹下的log文件之中
'''

#对应接口：游客登录 -- http://passportapi.15166.com/login-new
class test_visitorLogin(unittest.TestCase):
    url = 'http://passportapi.qa.15166.com/login-new'                                       #所要访问的url,一个测试类对应一个url
    appkey = 'f46806d675f16feae23b5c07d4a3c935' 

    def setUp(self):                                                                        #文件/数据库/网络服务初始化工作
        pass

    def tearDown(self):                                                                     #销毁工作
        pass

    def test_visitorLogin_cases(self):                                                      #执行测试功能的函数
        with open('csv/visitorLogin_data.csv') as csvfile:                                  #打开csv文件流
            reader = csv.DictReader(csvfile)                                                #创建文件流对象
            signup_num=0                                                                    #计算一共跑了多少条测试数据
            for row in reader:                                                              #这里的row对应csv表里的一行数据,第一行数据自动作为字段名,第二行数据开始作为测试实例
                signup_num+=1                                                         
                with self.subTest(row=row):                                                 #row=i,会报错row is not defined,必须用row=row(这里用的是subTest功能)
                    print("正在为'游客登录接口'执行第 %d 条测试数据"%signup_num)            #每跑一条数据,显示一次当前进度
                    
                    info = {
                            'action': row['action'], 
                            'appId': row['appId'], 
                            'guid': row['guid'], 
                            'channel': row['channel'], 
                            'signature': row['signature'], 
                            'subChannel': row['subChannel']
                            }                                                               #csv里的每一行测试实例，这里不用过滤空值，空值可以作为测试用例，引发异常
                    
                    sign_data = info['appId']+info['guid']+info['channel']+test_visitorLogin.appkey        
                    sign = hashlib.md5()                                                    # 生成signature
                    sign.update(sign_data.encode('utf-8'))
                    sign_md5_data = sign.hexdigest()
                    info['signature'] = sign_md5_data 
                    
                    postdata = urllib.parse.urlencode(info).encode('utf-8')                 # 将信息编码成urllib能够识别的类型,注意的是python2.7用的ASCII编码,python3.X要UTF8转码 
                    response = urllib.request.urlopen(self.url, postdata).read()            # 服务器响应的字符串消息
                    response_dict = json.loads(response.decode())                           # json转换成字典
                    # print(response_dict)

                    self.assertEqual(response_dict['code'], eval(row['code']))              #游客登录接口---您看到此信息,代表当行测试数据未通过---  
                 
        print("----------------------------------------------------------------------------------------------------------------------")
    


'''
unittest.main(),固定格式,用于默认调用unittest模块

'''

if __name__ == '__main__':
    
    '''
    如果是想输出重定向，则用此块代码
    log_file = 'log/log_%s.txt'%time.strftime('%Y_%m_%d_%H:%M:%S', time.localtime()) #定义log路径及文件名
    f = open(log_file, 'w')
    runner = unittest.TextTestRunner(f)
    unittest.main(testRunner=runner)
    f.close()
    
    '''

    unittest.main()
