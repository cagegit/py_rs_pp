from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import json
import random
import os
from PIL import Image
from log import logger


# errorList = []
# successList = []
# currentLine = 0


# 三组账号
def change_bank_account():
    numStr = '0123456789'
    keys = ['031100209', '124303162', '071006651']
    dian = {'124303162': '693636', '031100209': '77723256665', '071006651': '8230010824'}
    idx = random.randint(0, 2)
    num_a = keys[idx]
    num_b = dian[num_a] + "".join(random.sample(numStr, 6))
    # 693636828770
    # 77723256665
    # 8230010824
    return [num_a, num_b]


'''
 法国注册类
'''


class DeRegister:
    # fileName = './register/secret.png'
    fileName = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'secret.png')
    lzUserName = 'cagejet_666'
    lzPassWord = 'cage@Lz888'
    retryMax = 3
    retryCount = 0
    accoutRetryCount = 0
    accoutRetryMax = 5
    successList = []
    errorList = []

    # account = []
    def __init__(self, url, acccout):
        self.errorList = []
        self.successList = []
        self.url = url
        self.account = acccout
        self.retryCount = 0
        logger.info(acccout)
        # self.userName = uName
        # self.passWord = uPass
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        self.options.add_argument("--disable-blink-features")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--window-size=1450,1516")

    def getElementBy(self, selector, t='id'):
        if t == 'css':
            return self.driver.find_element_by_css_selector(selector)
        else:
            return self.driver.find_element_by_id(selector)

    # 保存验证码到图片
    def get_code_image(self, selector):
        isDone = False
        try:
            code_element = self.driver.find_element_by_css_selector(selector)
            self.driver.save_screenshot(self.fileName)
            # scrollTop = self.driver.execute_script("return document.documentElement.scrollTop")
            # print(scrollTop)
            left = code_element.location['x']
            top = code_element.location['y']
            print(left)
            print(top)
            right = code_element.size['width'] + left
            height = code_element.size['height'] + top
            im = Image.open(self.fileName)
            img = im.crop((left, top, right, height))
            img.save(self.fileName)
            logger.info('验证码图片保存成功!')
        except Exception as e:
            print(e)
            logger.error('验证码图片保存失败！', exc_info=True)
        else:
            isDone = True
            # yzmImg = self.driver.find_element_by_css_selector(selector)
        # if yzmImg:
        #     imgSrc = yzmImg.get_attribute('src')
        #     print(imgSrc)

        #     try:
        #         # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'}
        #         # s = requests.session()
        #         # resp = s.get(url, headers=headers, verify=False)
        #         r = requests.get(imgSrc)
        #         # 将获取到的图片二进制流写入本地文件
        #         with open(self.fileName, 'wb') as f:
        #             f.write(r.content)
        #     except Exception as e:
        #         print(e)
        #         print('写入文件失败！')
        #     else:
        #         isDone = True
        # else:
        #     print('获取图片失败！')
        return isDone

    # 识别图片验证码并返回验证码
    def get_code_text(self):
        # api_username, api_password, file_name, api_post_url, yzm_min, yzm_max, yzm_type, tools_token
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
            'Connection': 'keep-alive',
            'Host': 'v1-http-api.jsdama.com',
            'Upgrade-Insecure-Requests': '1'
        }
        files = {
            'upload': ('secret.png', open(self.fileName, 'rb'), 'image/png')
        }

        data = {
            'user_name': self.lzUserName,
            'user_pw': self.lzPassWord,
            'yzm_minlen': '5',
            'yzm_maxlen': '7',
            'yzmtype_mark': '1013',
            'zztool_token': '4ed2e5863384db8d6c43d8c9ea253ab2'
        }
        s = requests.session()
        # r = s.post(api_post_url, headers=headers, data=data, files=files, verify=False, proxies=proxies)
        api_post_url = 'http://v1-http-api.jsdama.com/api.php?mod=php&act=upload'
        r = s.post(api_post_url, headers=headers, data=data, files=files, verify=False, timeout=(15, 20))
        logger.info('图片验证码识别结果:')
        logger.info(r)
        return r.text

    def play(self):
        driver_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'driver',
                                   'chromedriver.exe')
        print(driver_path)
        self.driver = webdriver.Chrome(executable_path=driver_path, options=self.options)
        self.driver.get(self.url)
        try:
            # 等待页面加载完成
            changeBtn = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#contact_info_edit_addy_link>a'))
            )
            # 点击change超链接 contact_info_edit_addy_link
            changeBtn.click()
            time.sleep(2)
            # First Name
            # 姓 1
            firstNameInput = self.getElementBy('first_name')
            # time.sleep(3)
            # print(firstNameInput)
            firstNameInput.send_keys(self.account[0])
            # Last Name
            # 名 2
            lastNameInput = self.getElementBy('last_name')
            # time.sleep(3)
            # print(lastNameInput)
            lastNameInput.send_keys(self.account[1])
            # Address line 1 #address1
            # 地址 3
            address1Input = self.getElementBy('address1')
            # time.sleep(3)
            # print(address1Input)
            address1Input.send_keys(self.account[2])
            # 邮编 4
            zipCodeInput = self.getElementBy('zip')
            # time.sleep(2)
            # print(zipCodeInput)
            zipCodeInput.send_keys(self.account[3])
            # Address line 2 可选
            # ZIP code
            # 城市 5
            cityInput = self.getElementBy('city')
            # time.sleep(3)
            # print(cityInput)
            cityInput.send_keys(self.account[4])
            # State
            # time.sleep(3)
            # # 城镇 9
            # stateSelect = self.getElementBy('state')
            # Select(stateSelect).select_by_value(self.account[9])  # 选择value="o2"的项
            # time.sleep(3)
            # print(stateSelect)
            # Date of birth
            # mm input #dob_a
            #
            dateMmInput = self.getElementBy('dob_a')
            # time.sleep(1)
            dateMmInput.send_keys(self.account[5])
            # dd input #dob_b
            dateDdInput = self.getElementBy('dob_b')

            dateDdInput.send_keys(self.account[6])
            # time.sleep(1)
            # yyyy input #dob_c
            datYyInput = self.getElementBy('dob_c')
            # time.sleep(1)
            datYyInput.send_keys(self.account[7])
            # 邮箱 1
            emailInput = self.getElementBy('email')
            # for w in self.account[11]:
            #   emailInput.send_keys(w)
            #   time.sleep(1)
            # time.sleep(1)
            emailInput.send_keys(self.account[11])
            # emailInput.send_keys(self.account[11])
            # password input #password
            # 密码 2
            passInput = self.getElementBy('password')
            time.sleep(1)
            passInput.send_keys(self.account[12])
            # for w in self.account[12]:
            #    passInput.send_keys(w)
            #    time.sleep(1)
            # Confirm Password input #retype_password
            # 确认密码 3
            rePassInput = self.getElementBy('retype_password')
            time.sleep(1)
            rePassInput.send_keys(self.account[12])
            # Phone input #H_PhoneNumber
            # 手机号码 9
            # phoneInput = self.getElementBy('H_PhoneNumber')
            # # time.sleep(2)
            # phoneInput.send_keys(self.account[8])
            # for w in self.account[8]:
            #   phoneInput.send_keys(w)
            #   time.sleep(1)
            # phoneInput.send_keys(self.account[8])
            # Email Address input #email

            # for w in self.account[12]:
            #     rePassInput.send_keys(w)
            #     time.sleep(1)
            # gl-test 防止弹框遮挡
            # textIns = self.getElementBy('gl-test');
            # self.driver.execute_script('document.getElementById("gl-test").click()') # 执行js语句
            # textIns.click();
            self.securityNumberInput = self.getElementBy('string_answer')
            self.securityNumberInput.send_keys('')
            # time.sleep(3)
            # 关键步骤 图片验证码
            # 验证码图片地址 img #gl-test-image>img
            self.driver.execute_script("document.body.click();")
            time.sleep(2)
            self.securityNumberInput.send_keys('')
            is_done = self.get_code_image("#gl-test-image>img")
            print('步骤1，生成验证码图片:')
            print(is_done)
            self.first_step()

        except TimeoutException:
            # print('Timeout!')
            logger.error('操作超时！该条数据可以重新使用', exc_info=True)
            self.errorList.append(self.account)
        except Exception as e:
            print(e)
            logger.error('代码出错！该条数据可以重新使用', exc_info=True)
            self.errorList.append(self.account)
        finally:
            logger.info('流程完毕！')
            # time.sleep(10)
            self.driver.quit()

    # 验证码重试三次
    def retry_yzm(self):
        if self.retryCount <= self.retryMax:
            self.retryCount = self.retryCount + 1
            logger.info('验证码重试，第%s次！' % self.retryCount)
            self.secondStep()
        else:
            logger.info('验证码识别重试%s次出错！' % self.retryMax)
            self.retryCount = 0
            self.errorList.append(self.account)

    # 第一步操作
    def first_step(self):
        securityNumberInput = self.getElementBy('string_answer')
        time.sleep(2)
        # security Measure input #string_answer
        # time.sleep(1);
        securityNumberInput.send_keys('abcdefg')
        # sign up input #signup
        # sign_up_btn = WebDriverWait(self.driver, 15).until(
        #     EC.element_to_be_clickable((By.ID, 'signup'))
        # )
        # sign_up_btn = self.getElementBy('signup')
        # time.sleep(3)
        # 点击注册 页面会刷新
        self.driver.execute_script("document.getElementById('signup').click();")
        time.sleep(3)
        self.secondStep()

    # 第二步 尝试
    def secondStep(self):
        try:
            pInput = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'password'))
            )
            pInput.send_keys(self.account[12])
            # for w in self.account[12]:
            #     pInput.send_keys(w)
            #     time.sleep(1)
            time.sleep(2)
            rpInput = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'retype_password'))
            )
            time.sleep(2)
            rpInput.send_keys(self.account[12])
            # rePassInput.send_keys(self.account[12])
            # for w in self.account[12]:
            #     rpInput.send_keys(w)
            #     time.sleep(1)
            security_number_input = self.getElementBy('string_answer')
            security_number_input.send_keys('')
            # time.sleep(3)
            is_done = self.get_code_image("#gl-test-image>img")
            logger.info('步骤2，生成验证码图片:')
            print(is_done)
            if is_done:
                try:
                    res_info = self.get_code_text()
                    text = json.loads(res_info)
                except Exception as e:
                    print(e)
                    logger.error('验证码返回json解析异常', exc_info=True)
                    text = {'data': {'val': None}, 'result': False}
                logger.info('de code 2:')
                logger.info(text['data'])
                if text['result']:
                    # time.sleep(5)
                    # security Measure input #string_answer
                    # time.sleep(1);
                    security_number_input.send_keys(text['data']['val'])
                    # sign up input #signup
                    # sign_up_btn = WebDriverWait(self.driver, 5).until(
                    #     EC.element_to_be_clickable((By.ID, 'signup'))
                    # )
                    # sign_up_btn = self.getElementBy('signup')
                    time.sleep(1)
                    # 点击注册 页面会刷新
                    self.driver.execute_script("document.getElementById('signup').click();")
                    time.sleep(5)
                    self.thirdStep()
                else:
                    logger.info('调用识别验证码接口出错，准备重试！')
                    if security_number_input:
                        security_number_input.send_keys('')
                    # self.get_code_image("#gl-test-image>img")
                    self.retry_yzm()
            else:
                logger.error('生成验证码图片失败！')
            time.sleep(10)
        except Exception as e:
            # 没有文本框说明已经跳转
            print(e)
            self.errorList.append(self.account)
            logger.error('第二次输入密码、验证码异常', exc_info=True)

    def fourStep(self):
        self.driver.get('https://www.paypal.com/us/webapps/mpp/pfs/welcome/offer')
        time.sleep(3)

    # 第三步
    def thirdStep(self):
        self.driver.get('https://www.paypal.com/myaccount/security/autologin')
        time.sleep(10)
        nextBtn = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, 'btnNext'))
        )
        if nextBtn:
            userNameInput = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, 'email'))
            )
            userNameInput.send_keys(self.account[11])
            nextBtn.click()
            time.sleep(5)
            passWordInput = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'password'))
            )
            time.sleep(3)
            passWordInput.send_keys(self.account[12])
        else:
            userNameInput = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, 'email'))
            )
            passWordInput = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, 'password'))
            )
            time.sleep(5)
            userNameInput.send_keys(self.account[11])
            time.sleep(3)
            passWordInput.send_keys(self.account[12])

        # 获取登录按钮
        submitBtn = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.ID, 'btnLogin'))
        )
        # 点击登录按钮
        # time.sleep(1)
        submitBtn.click()
        time.sleep(5)
        self.driver.get('https://www.paypal.com/myaccount/money/banks/new?type=MANUAL')
        # time.sleep(5)
        # 重试多次银行卡绑定
        self.shuruBankCard()
        # self.driver.get('https://www.paypal.com/')
        # self.fourStep()

    # 输入银行卡
    def shuruBankCard(self):
        acc_list = change_bank_account()
        # print()
        routingNumberInput = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, 'routingNumberGroup'))
        )
        time.sleep(2)
        routingNumberInput.send_keys(acc_list[0])
        accountNumberInput = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, 'accountNumberInput'))
        )
        time.sleep(2)
        accountNumberInput.send_keys(acc_list[1])
        subBtn = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[name="addBank"]'))
        )
        subBtn.click()
        time.sleep(5)
        rnInput = None
        try:
            logger.info('输入银行卡步骤，获取rnInput')
            rnInput = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, 'routingNumberGroup'))
            )
        except Exception as e:
            logger.error('获取rnInput异常', exc_info=True)
            print(e)
        # print(rnInput)
        if rnInput:
            self.retryAccount()
        else:
            # pendingConfirmBank
            time.sleep(5)
            logger.info('注册流程成功！-----------------------------')
            self.successList.append(self.account)
            self.fourStep()
            # continueBtn = self.getElementBy('PayPalCDVButtonText')
            # if continueBtn:
            #     try:
            #         continueBtn.click()
            #         time.sleep(5)
            #     except Exception as e:
            #         print(e)
            # okBtn = self.getElementBy('button[name="pendingConfirmBank"]','css')
            # if okBtn:
            #     okBtn.click()
            #     time.sleep(5)
            #     self.fourStep()
            # else:
            #     self.fourStep()

    # 银行卡重试
    def retryAccount(self):
        if self.accoutRetryCount <= self.accoutRetryMax:
            self.accoutRetryCount = self.accoutRetryCount + 1
            self.shuruBankCard()
        else:
            self.fourStep()


if __name__ == '__main__':
    # 德国
    deUrl = 'https://www.paypal.com/de/cgi-bin/webscr?cmd=_integrated-registration&ev=1.9&locale=de_DE&fdata=Ul58zj%2FYbie6f5ipBaS3hwrSfch%2BEdmdbGxSK1cadSrbpe9W3Od6p%2FMcMP7kRwA4t97Ug4W0jufoT8737J6uGg%3D%3D#'
