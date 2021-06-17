import time
import os
'''
 写入成功文档
'''
class AccountRecordSuccess:
  success_path = './register/success/'
  
  # 二维数组
  def __init__(self,success_list,file_path = ''):
    if file_path != '':
      self.success_path = file_path
         
    current_date = time.strftime("%Y-%m-%d_%H时%M分", time.localtime())
    file_name = current_date + '_注册成功账号列表.txt'
    if os.path.exists(self.success_path + file_name):
      with open(self.success_path + file_name, 'a') as file:
        for item in success_list:
          current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
          # info = ''
          # for key in item:
          #   info = info + key + ':' + item[key] + ' '
          itemStr = ",".join([str(x) for x in item])
          file.writelines(current_time + ','+ itemStr + '\n')  
        file.close()
    else:
      with open(self.success_path + file_name, 'w+') as file:
        for item in success_list:
          current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
          # info = ''
          # for key in item:
          itemStr = ",".join([str(x) for x in item])
          file.writelines(current_time + ','+ itemStr + '\n')  
        file.close()

'''
 写入错误文档
'''
class AccountErrorRecord:
  error_path = './register/error/'  
  def __init__(self,error_list,file_path = ''):
    if file_path != '':
      self.error_path = file_path
      
    current_date = time.strftime("%Y-%m-%d_%H时%M分", time.localtime())
    file_name = current_date + '_注册失败账号列表.txt'
    if os.path.exists(self.error_path + file_name):
      with open(self.error_path + file_name, 'a') as file:
        for item in error_list:
          current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
          itemStr = ",".join([str(x) for x in item])
          file.writelines(current_time + ','+ itemStr + '\n')   
        file.close()
    else:
      with open(self.error_path + file_name, 'w+') as file:
        for item in error_list:
          current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
          itemStr = ",".join([str(x) for x in item])
          file.writelines(current_time + ','+ itemStr + '\n') 
        file.close()

'''
 写入错误文档
'''
class AccountErrorSingleRecord:
  error_path = './register/error/'  
  def __init__(self,error_list,file_path = ''):
    if file_path != '':
      self.error_path = file_path
      
    current_date = time.strftime("%Y-%m-%d", time.localtime())
    file_name = current_date + '_注册失败账号列表.txt'
    if os.path.exists(self.error_path + file_name):
      with open(self.error_path + file_name, 'a') as file:
        for item in error_list:
          current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
          itemStr = ",".join([str(x) for x in item])
          file.writelines(current_time + ','+ itemStr + '\n')   
        file.close()
    else:
      with open(self.error_path + file_name, 'w+') as file:
        for item in error_list:
          current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
          itemStr = ",".join([str(x) for x in item])
          file.writelines(current_time + ','+ itemStr + '\n') 
        file.close()

                 