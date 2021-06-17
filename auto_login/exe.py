import subprocess
import win32clipboard
import win32gui
user32 = windll.user32
hwnd = user32.GetForegroundWindow()
print(hwnd)
proc = subprocess.Popen(["cmd","/C","ping","www.baidu.com"],shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
print('run:')
print(proc)
try:
    out,err = proc.communicate(timeout=15)
    # proc.wait()
    status = proc.wait()
    print("cmd out: ", out.decode('gbk'))
    if(err):
      print(err)
except:
    proc.kill()
    outs, errs = proc.communicate()
    print(errs)
else:
    print('finally')  
    proc.kill()
      