import requests;
import random
import string
passStr=string.ascii_letters+string.digits+'@#$&'
emailStr = string.ascii_letters+string.digits+'_'
emailHz = ['hotmail.com','mail.com','yahoo.com','gmail.com']
numStr = '0123456789'
# key=[]
def genPassword():
	key=random.sample(passStr,random.randint(8,15))
	keys="".join(key)
	return keys

def genEmail():
  key=random.sample(emailStr,random.randint(6,12))
  keys="".join(key)
  return keys + '@' +emailHz[random.randint(0,3)]

def changeBankAccount():
     keys = ['031100209','124303162','071006651']
     dian = {'124303162':'693636','031100209':'77723256665','071006651':'8230010824'}
     idx = random.randint(0,2)
     num_a = keys[idx]
     num_b = dian[num_a] + "".join(random.sample(numStr,6))
     # 693636828770
     # 77723256665
     # 8230010824
     return [num_a,num_b] 

def getImage():
    url = "https://www.paypal.com/cgi-bin/gs_web/ysKCYdIHCaq7JQZsau5kRPHoaEud0Ko5VsuaTmm65VnBwziH5-kRmqvlDxmoDKG5H2iOWw/secret.jpeg"
    res = requests.get(url,verify=False)
    print(res)

class makeList:      
  # 声明一个空数组，来保存文本文件数据
  account_list = []
  done_list = []
  error_list = []
  def __init__(self, filePath):
      print('init')
      try: 
        # 打开文本文件
        file = open(filePath,'r')
        # 遍历文本文件的每一行，strip可以移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
        for line in file.readlines():
            line = line.strip()
            item = line.split('----')[1:]
            print(item)
            item.append(genEmail())
            pwd = genPassword()
            item.append(pwd)
            self.account_list.append(item)
        file.close()
      except Exception:
        raise Exception("打开文件异常,请确保user.txt文件在account目录")
    

if __name__ == '__main__':    
    # ins = makeList('./register/usa.txt');
    # print(ins.account_list)
    # # for item in range(10):
    # #     print(genPassword())
    # # for item in range(10):
    # #     print(genEmail())
    # #    ins
    # getImage()
    for item in range(10):
       print(changeBankAccount())