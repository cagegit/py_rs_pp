   
'''
 用户文件读取类
'''
class ReadAccountToArray: 
  # 声明一个空数组，来保存文本文件数据
  account_list = []
  done_list = []
  error_list = []
  def __init__(self, filePath):
      print('init')
      try: 
        # 打开文本文件
        file = open(filePath, 'r')
        # 遍历文本文件的每一行，strip可以移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
        for line in file.readlines():
            line = line.strip()
            k = line.split(' ')[0]
            v = line.split(' ')[1]
            self.account_list.append({'name': k, 'password': v})
        file.close()
      except Exception:
        raise Exception("打开文件异常,请确保user.txt文件在account目录")