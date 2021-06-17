import random
import string
passStr = string.ascii_letters
passNum = string.digits
passSymbol ='@#$&#!_'
emailStr = string.ascii_letters+string.digits+'_'
emailHz = ['hotmail.com','mail.com','yahoo.com','gmail.com']
# 生成密码
def genPassword():
    key=random.sample(passStr,random.randint(5,10))
    key.extend(random.sample(passNum,random.randint(2,6)))
    key.extend(random.sample(passSymbol,random.randint(1,4)))
    # key[random.randint(1,len(key)-1)] = "$"
    # print(key)
    random.shuffle(key)
    keys="".join(key)
    return keys

# 生成邮箱
def genEmail():
  key=random.sample(emailStr,random.randint(6,12))
  keys="".join(key)
  return keys + '@' +emailHz[random.randint(0,3)]   
'''
 读取账号文件到数组
'''
class LoadAccountToArray: 
  # 声明一个空数组，来保存文本文件数据
  account_list = []
  done_list = []
  error_list = []
  def __init__(self, filePath,fengefu):
      print('init')
      # 打开文本文件
      with open(filePath,'r') as r:
        # 遍历文本文件的每一行，strip可以移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
        for line in r.readlines():
            line = line.strip()
            account = line.split(fengefu)
            account.append(genEmail())
            account.append(genPassword())
            if len(account) > 0:
               self.account_list.append(account[1:])
        
# 测试
if __name__ == '__main__':    
    ins = LoadAccountToArray('./register/usa.txt','----'); 
    for item in ins.account_list:
        print(item)   
    # for x in range(10):
    #     print(genPassword())  