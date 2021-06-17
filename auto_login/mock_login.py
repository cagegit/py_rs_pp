from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import re

# 替换字符串里面非数字小数点的内容
numReg = re.compile('[^0-9\.]')

'''
 模拟登录类
'''
class MockWeb: 
  isDone = False
  url = ''
  userName = ''
  passWord = ''
  def __init__(self,url,uName,uPass):
      # url = 'https://www.paypal.com/'
      self.url = url
      self.userName = uName
      self.passWord = uPass
      self.options = webdriver.ChromeOptions()
      self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
      self.options.add_experimental_option('useAutomationExtension', False)
      self.options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
      self.options.add_argument("--disable-blink-features")
      self.options.add_argument("--disable-blink-features=AutomationControlled")
      self.options.add_argument("--window-size=1450,936")
      # # 设置代理
      # self.options.add_argument("--proxy-server=http://172.21.0.14:5000")
      # options.add_argument("--lang=en")
    # 美国账号流程  
  def runUs(self):
      self.driver = webdriver.Chrome(options=self.options)
      self.driver.get(self.url)
      print('打开浏览器')
      # time.sleep(100)
      try:
        #  获取登录按钮
        # loginBtn = WebDriverWait(self.driver, 15).until(
        #   EC.element_to_be_clickable((By.CSS_SELECTOR, '#ul-btn.pypl-btn'))
        # )
        # print('得到登录按钮入口')    
        # loginBtn.click()
        time.sleep(2)
        nextBtn = WebDriverWait(self.driver, 5).until(
          EC.presence_of_element_located((By.ID, 'btnNext'))
        )
        if nextBtn:
          userNameInput = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, 'email'))
          )
          userNameInput.send_keys(self.userName)
          nextBtn.click() 
          time.sleep(3)
          passWordInput = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'password'))
          )
          time.sleep(3)
          passWordInput.send_keys(self.passWord)
        else:
          userNameInput = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, 'email'))
          ) 
          passWordInput = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, 'password'))
          )
          time.sleep(3)
          userNameInput.send_keys(self.userName)
          time.sleep(3)
          passWordInput.send_keys(self.passWord)
        
        # 获取登录按钮  
        submitBtn = WebDriverWait(self.driver, 5).until(
          EC.element_to_be_clickable((By.ID, 'btnLogin'))
        )
        # 点击登录按钮
        time.sleep(1)
        submitBtn.click()
        time.sleep(10)
        self.driver.get('https://www.paypal.com/')
        # 查看余额，有余额继续支付，没有余额，退出
        time.sleep(10)
        # 两种情况登录成功或者登录失败，登录失败获取付款按钮失败超时退出
        # 获取付款菜单
        transferLinkBtn = WebDriverWait(self.driver, 10).until(
          EC.element_to_be_clickable((By.CSS_SELECTOR, 'a#header-transfer'))
        )
        transferLinkBtn.click()
        time.sleep(20)
        self.isDone = True
        print('game over!')
      except TimeoutException:
        print('Timeout!')
      finally:
        self.driver.close()
        print('不退出')
        return self.isDone
  # 德国账号流程      
  def runDe(self):
    self.driver = webdriver.Chrome(options=self.options)
    self.driver.get(self.url)
    print('打开浏览器')
    # time.sleep(100)
    try:
      #  获取登录按钮
      # loginBtn = WebDriverWait(self.driver, 15).until(
      #   EC.element_to_be_clickable((By.CSS_SELECTOR, '#ul-btn.pypl-btn'))
      # )
      # print('得到登录按钮入口')    
      # loginBtn.click()
      time.sleep(2)
      nextBtn = WebDriverWait(self.driver, 5).until(
        EC.presence_of_element_located((By.ID, 'btnNext'))
      )
      if nextBtn:
        userNameInput = WebDriverWait(self.driver, 5).until(
          EC.presence_of_element_located((By.ID, 'email'))
        )
        userNameInput.send_keys(self.userName)
        nextBtn.click() 
        time.sleep(5)
        passWordInput = WebDriverWait(self.driver, 10).until(
          EC.presence_of_element_located((By.ID, 'password'))
        )
        time.sleep(5)
        passWordInput.send_keys(self.passWord)
      else:
        userNameInput = WebDriverWait(self.driver, 5).until(
          EC.presence_of_element_located((By.ID, 'email'))
        ) 
        passWordInput = WebDriverWait(self.driver, 5).until(
          EC.presence_of_element_located((By.ID, 'password'))
        )
        time.sleep(5)
        userNameInput.send_keys(self.userName)
        time.sleep(5)
        passWordInput.send_keys(self.passWord)
      
      # 获取登录按钮  
      submitBtn = WebDriverWait(self.driver, 5).until(
        EC.element_to_be_clickable((By.ID, 'btnLogin'))
      )
      # 点击登录按钮
      time.sleep(2)
      submitBtn.click()
      time.sleep(15)
      self.driver.get('https://www.paypal.com/')
      # 查看余额，有余额继续支付，没有余额，退出
      time.sleep(10)
      yueSpan = WebDriverWait(self.driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'span.cw_tile-currency'))
      )
      mon = yueSpan.get_attribute('innerText')
       # 两种情况登录成功或者登录失败，登录失败获取付款按钮失败超时退出
      if mon :
        mon = float(numReg.sub('', mon))
        print(mon)
        # 判断金额大于等于5，进行后续转款操作，不满足条件直接退出
        if mon >= 5:
          # 获取付款菜单
          transferLinkBtn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a#header-transfer'))
          )
          transferLinkBtn.click()
          # 等待付款页面完全加载
          time.sleep(2)
          fkAccountInput = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input#fn-sendRecipient'))
          )
          # 输入收款账号
          fkAccountInput.send_keys('')
          time.sleep(5)
          continueBtn = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.ppvx_btn___5-6-1'))
          )
          # 点击继续按钮
          time.sleep(3)
          continueBtn.click()
          time.sleep(1)
          # 进入输入付款金额
          fkJeInput = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input#fn-senderPaysAmount'))
          )
          for num in [5,0,0]:
              fkJeInput.send_keys(num)
              time.sleep(1)
          continueStep2Btn = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.ppvx_btn___5-6-1'))
          )
          # 第二个继续按钮
          continueStep2Btn.click()
        else:
          self.isDone = False    
          print('余额不足')     
      else :
        self.isDone = False
        
      print('game over!')
    except TimeoutException:
      print('Timeout!')
    finally:
      self.driver.close()
      print('不退出')
      return self.isDone

  def close(self):
    if self.driver:
      self.driver.close() 