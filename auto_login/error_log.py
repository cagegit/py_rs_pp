import time
import os


'''
 写入错误文档
'''
class WriteErrorLog: 
  def __init__(self,error_list):
    current_date = time.strftime("%Y-%m-%d", time.localtime())
    file_name = current_date + '_error.log'
    if os.path.exists('./log/' + file_name):
      with open('./log/' + file_name, 'a') as file:
        for item in error_list:
          current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
          info = ''
          for key in item:
            info = info + key + ':' + item[key] + ' '
          file.writelines(current_time + ' '+ info + '\n')  
        file.close()
    else:
      with open('./log/' + file_name, 'w+') as file:
        for item in error_list:
          current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
          info = ''
          for key in item:
            info = info + key + ':' + item[key] + ' '
          file.writelines(current_time + ' '+ info + '\n')
        file.close()