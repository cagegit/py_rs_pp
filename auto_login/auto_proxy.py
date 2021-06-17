import subprocess
import time
'''
自动切换911 s5代理
'''
class AutoOldChangeProxy:
  # exe = r'C:\Users\Administrator\Documents\911\ProxyTool\Autoproxytool.exe'
  exe = r'C:\Users\Administrator\Documents\911\ProxyTool\AutoProxyTool.exe'
  # param = r' -changeproxy/US/NY -proxyport=all -hwnd=test';
  # proc = subprocess.Popen([exe,'-changeproxy/','-ip=23.*.*.*'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  def __init__(self):
    print('auto_proxy change init!')
  
  def change_ip(self,country='US',ip="23.*.*.*"):
    # param = r' -changeproxy/US/NY -proxyport=all -hwnd=test';
    proc = subprocess.Popen([self.exe,'-changeproxy/'+ country,'-ip=' + ip],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    # proc = subprocess.Popen([arg,'-changeproxy/US/NY','-freeport=all'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    print('auto_proxy is runing...')
    isDone = False
    try:
        out,err = proc.communicate(timeout=15)
        # proc.wait()
        proc.wait()
        print("out: ", out)
        if(err):
          isDone = False
          print('代理出错:')
          print(err)
        # 等待3秒 等待程序ip切换完成  
        time.sleep(3)  
        isDone = True  
    except:
        proc.kill()
        isDone = False
        print('切换代理出错了')
    finally:
        print('结束流程')  
        proc.kill() 
    return isDone     
      