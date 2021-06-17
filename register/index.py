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

numStr = '0123456789'
# errorList = []
# successList = []
currentLine = 0


# 三组账号
def change_bank_account():
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
 模拟注册类
'''


class Register:
    fileName = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'secret.png')
    lzUserName = 'cagejet_666'
    lzPassWord = 'cage@Lz888'
    retryMax = 3
    retryCount = 0
    accoutRetryCount = 0
    accoutRetryMax = 5
    errorList = []
    successList = []

    # account = []
    def __init__(self, url, acccout):
        self.errorList = []
        self.url = url
        self.account = acccout
        self.retryCount = 0
        # self.userName = uName
        # self.passWord = uPass
        logger.info(acccout)
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
            print('image done!')
        except Exception as e:
            print(e)
            print('获取图片失败！')
        else:
            isDone = True
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
        print('get_code_text:')
        print(r)
        return r.text

    def play(self):
        # webdriver.Chrome(driver, options=)
        driver_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'driver', 'chromedriver.exe')
        print(driver_path)
        self.driver = webdriver.Chrome(executable_path=driver_path, options=self.options)
        self.driver.get(self.url)
        try:
            # 等待页面加载完成
            changeBtn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#contact_info_edit_addy_link>a'))
            )
            # 点击change超链接 contact_info_edit_addy_link
            changeBtn.click()
            time.sleep(2)
            # First Name
            firstNameInput = self.getElementBy('first_name')
            # time.sleep(3)
            print(firstNameInput)
            firstNameInput.send_keys(self.account[0])
            # Last Name
            lastNameInput = self.getElementBy('last_name')
            # time.sleep(3)
            print(lastNameInput)
            lastNameInput.send_keys(self.account[1])
            # Address line 1 #address1
            address1Input = self.getElementBy('address1')
            # time.sleep(3)
            print(address1Input)
            address1Input.send_keys(self.account[2])
            # Address line 2 可选
            # ZIP code 
            zipCodeInput = self.getElementBy('zip')
            # time.sleep(2)
            print(zipCodeInput)
            zipCodeInput.send_keys(self.account[3])
            # CITY
            cityInput = self.getElementBy('city')
            # time.sleep(3)
            print(cityInput)
            cityInput.send_keys(self.account[4])
            # State
            # time.sleep(3)
            stateSelect = self.getElementBy('state')
            Select(stateSelect).select_by_value(self.account[9])  # 选择value="o2"的项
            # time.sleep(3)
            print(stateSelect)
            # Date of birth
            # mm input #dob_a
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
            # Phone input #H_PhoneNumber
            phoneInput = self.getElementBy('H_PhoneNumber')
            # time.sleep(2)
            phoneInput.send_keys(self.account[8])
            # for w in self.account[8]:
            #   phoneInput.send_keys(w) 
            #   time.sleep(1)
            # phoneInput.send_keys(self.account[8])
            # Email Address input #email
            emailInput = self.getElementBy('email')
            # for w in self.account[11]:
            #   emailInput.send_keys(w) 
            #   time.sleep(1)
            # time.sleep(1)
            emailInput.send_keys(self.account[11])
            # emailInput.send_keys(self.account[11])
            # password input #password
            passInput = self.getElementBy('password')
            time.sleep(1)
            passInput.send_keys(self.account[12])
            # for w in self.account[12]:
            #    passInput.send_keys(w) 
            #    time.sleep(1)
            # Confirm Password input #retype_password
            rePassInput = self.getElementBy('retype_password')
            time.sleep(1)
            rePassInput.send_keys(self.account[12])
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
            logger.error('操作超时！该条数据可以重新使用', exc_info=True)
            self.errorList.append(self.account)
        except Exception as e:
            print(e)
            logger.error('代码出错！该条数据可以重新使用', exc_info=True)
            self.errorList.append(self.account)
        finally:
            print('流程完毕！')
            # time.sleep(10)
            self.driver.quit()
            # 验证码重试三次

    def retry_yzm(self):
        if self.retryCount <= self.retryMax:
            self.retryCount = self.retryCount + 1
            logger.info('验证码重试第%s次！' % self.retryCount)
            self.secondStep()
        else:
            logger.info('验证码重试%s次出错！' % self.retryMax)
            self.retryCount = 0
            self.errorList.append(self.account)

    # 第一步操作
    def first_step(self):
        securityNumberInput = self.getElementBy('string_answer')
        time.sleep(1)
        # security Measure input #string_answer
        # time.sleep(1);
        securityNumberInput.send_keys('opqrs')
        # sign up input #signup
        signUpBtn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'signup'))
        )
        # time.sleep(3)
        # 点击注册 页面会刷新
        signUpBtn.click()
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
            rpInput = WebDriverWait(self.driver, 5).until(
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
            time.sleep(3)
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
                logger.info('us code 2:')
                logger.info(text['data'])
                if text['result']:
                    # time.sleep(5)
                    # security Measure input #string_answer
                    # time.sleep(1);
                    security_number_input.send_keys(text['data']['val'])
                    # sign up input #signup
                    signUpBtn = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.ID, 'signup'))
                    )
                    time.sleep(1)
                    # 点击注册 页面会刷新
                    signUpBtn.click()
                    time.sleep(5)
                    self.thirdStep()
                else:
                    logger.info('调用识别验证码接口出错，准备重试！')
                    if security_number_input:
                        security_number_input.send_keys('')
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
            print('获取rnInput')
            rnInput = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, 'routingNumberGroup'))
            )
        except Exception as e:
            print('获取rnInput异常')
            print(e)
        print(rnInput)
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
    # 美国
    webUrl = 'https://www.paypal.com/us/cgi-bin/webscr?cmd=_integrated-registration&ev=1.9&locale=us_US&fdata=Ul58zj%2FYbie6f5ipBaS3hwrSfch%2BEdmdbGxSK1cadSrbpe9W3Od6p%2FMcMP7kRwA4t97Ug4W0jufoT8737J6uGg%3D%3D#'
    # 法国
    frUrl = 'https://www.paypal.com/fr/cgi-bin/webscr?cmd=_integrated-registration&ev=1.9&locale=fr_FR&fdata=Ul58zj%2FYbie6f5ipBaS3hwrSfch%2BEdmdbGxSK1cadSrbpe9W3Od6p%2FMcMP7kRwA4t97Ug4W0jufoT8737J6uGg%3D%3D#'
    # 西班牙
    esUrl = 'https://www.paypal.com/es/cgi-bin/webscr?cmd=_integrated-registration&ev=1.9&locale=es_ES&fdata=Ul58zj%2FYbie6f5ipBaS3hwrSfch%2BEdmdbGxSK1cadSrbpe9W3Od6p%2FMcMP7kRwA4t97Ug4W0jufoT8737J6uGg%3D%3D#'
    # 德国
    deUrl = 'https://www.paypal.com/de/cgi-bin/webscr?cmd=_integrated-registration&ev=1.9&locale=de_DE&fdata=Ul58zj%2FYbie6f5ipBaS3hwrSfch%2BEdmdbGxSK1cadSrbpe9W3Od6p%2FMcMP7kRwA4t97Ug4W0jufoT8737J6uGg%3D%3D#'
    # 英国
    ukUrl = 'https://www.paypal.com/uk/cgi-bin/webscr?cmd=_integrated-registration&ev=1.9&locale=uk_UK&fdata=Ul58zj%2FYbie6f5ipBaS3hwrSfch%2BEdmdbGxSK1cadSrbpe9W3Od6p%2FMcMP7kRwA4t97Ug4W0jufoT8737J6uGg%3D%3D#'
    # accList = [['Haley', 'Maliszewski', '50, N Lake Dr', '14127', 'ORCHARD PARK', '07', '16', '1995', '17167836323', 'NY', '096842362', 'pzVSJ0G2m@mail.com', 'JetCage@1234'], ['cheryl', 'hendrickson', '75 bank st. #4p', '10014', 'NEW YORK', '06', '21', '1960', '19175440458',
    # 'NY', '565351986', 'vg1NhjSqnp@hotmail.com', 'UserInfo@123'], ['CATHERINE', 'PELLEGRINO', '168 RENKEN BLVD', '11010', 'FRANKLIN SQUARE', '03', '11', '1958', '15163287448', 'NY', '077545415', 'c2tw0gzM@yahoo.com', 'UserInfo@123'], ['michelle', 'Hamilton', '1141 east 221 st', '10469', 'BRONX', '05', '27', '1989', '13474656097', 'NY', '088983385', 'atGu6QbTBgJF@mail.com', 'UserInfo@@123'], ['Edward', 'Adu Nti', '1316E 224th St.', '10466', 'BRONX', '12', '24', '1964', '19178476292', 'NY', '111907729', 'YgxbrGl7k_@hotmail.com', 'jadXB61uc&8DTgzn'], ['Joy', 'Mika', '23 Bridgewater Way', '12601', 'Poughkeepsie', '01', '27', '1969', '18452401769', 'NY', '109684172', 'Rr3zvcsqO@mail.com', '65Vw@9Ehs'], ['Yamil', 'Melendez', '404 W 8TH St', '14701', 'Jamestown', '12', '26', '1984', '17164507041', 'NY', '597225042', 'Hv2cXfwDa@mail.com', 'yhA5xY#zrqd4'], ['Jennifer', 'Oquendo', '20 Cedar Street', '10701', 'YONKERS', '03', '13', '1991', '19148986516', 'NY', '097788813', 'WNRHnjqUZ9@gmail.com', 'tRK0uo#egO'], ['Christine', "O'Dee", '4271 Robin Lane', '14075', 'HAMBURG', '05', '17', '1965', '17163197477', 'NY', '073644404', 'jGSpqiZP@hotmail.com', 'SCB#6YkR']]
    # ins = LoadAccountToArray('./register/usa/100us.txt','----')
    # for item in ins.account_list:
    #     print(item)   
    # print(ins.account_list)
    #     accList = [['ABDUL', 'HARUNA', '1951 Niagara street', '14303', 'NIAGARA FALLS', '02', '23', '1978', '17165146238', 'NY', '811144011', 'beQ3iCz@gmail.com', 'N30B7qw8G1$V_9'], ['Ramon', 'Rohena', '1024 north main st', '14701', 'Jamestown', '06', '10', '1993', '17169699387', 'NY', '596408208', 'IgyOfXZtY8k@gmail.com', '2C0m6z!SB'], ['Gabriel', 'Nunez', '325 W 93rd St Apt 3D', '10025-7240', 'New York', '09', '22', '1974', '16469016065', 'NY', '061620316', 'gibK2txlrR@hotmail.com', 'G#yac1_0C'], ['Faigy', 'Berkovits', '5309 12th Ave Apt 2', '11219-3429', 'Brooklyn', '04', '15', '1968', '17184356748', 'NY', '057667243', 'PI_X0qe@hotmail.com', '25i$08@4uoyq1#vL'], ['Ana', 'Rodriguez', '3003 Wallace Ave', '10467', 'Bronx', '06', '18', '1988', '19148004209', 'NY', '115800336', 'WYnUDmfp@gmail.com', '9N8HJXE1G&_SI!'], ['John', 'Lundberg', '40 Logans Run', '14626', 'Rochester', '05', '16', '1969', '15858310214', 'NY', '061707610',
    # '81kpO64Fnq@mail.com', 'L@w10y!$WH#'], ['Christopher', 'Foster', '9604 state route 36', '14437', 'DANSVILLE', '09', '07', '1979', '16073821386', 'NY', '060682269', 'HB6N0aWAbp3O@yahoo.com', 'Xq#R9j1lI3Yidc'], ['Candice', 'Bravo-DiStefano', '114 Noel Drive', '11720', 'CENTEREACH', '03', '24', '1979', '16314282944', 'NY', '109968559', 'KuUpqyR@gmail.com', 's27zTWi_#$9x@u'], ['Ashley', 'Minella', '3640 Bronx Blvd', '10467', 'BRONX', '03', '23', '2001', '19292173280', 'NY', '095908153', '5aRuQSFsk3@yahoo.com', 'lQ_r8P0o63i!J5#'], ['Ian', 'Smithwrick', '120 stonelea place', '10801', 'NEW ROCHELLE', '08', '22', '1989', '16463001317', 'NY', '088765705', 'hc2PfIpmo@yahoo.com', 'C2LdW@4h1x30'], ['Andrew', 'Lewars', '2148 Schenectady Ave', '11234', 'BROOKLYN', '07', '23', '1981', '17183380197', 'NY', '086762792', 'dT5Ob8uzVZno@hotmail.com', 'EO19#Z5C&V07_a6U'], ['Princess', 'Pancubit', '343 Gold s', '11201', 'BROOKLYN',
    # '12', '03', '1996', '18312782304', 'NY', '616942462', 'vXYRtyU_nWc@yahoo.com', 'wk#P$j2HW67uVr0A'], ['Stephen', 'Rigos', '1418 Astoria Park S', '11102', 'Astoria', '10', '28', '1990', '16317428158', 'NY', '073785017', 'CjXOQZYws@yahoo.com', '98hkfEHYg@V'], ['Catherine', 'Reith', '1075 Edison Avenue 6D', '10465', 'Bronx', '05', '21', '1945', '16463281468', 'NY', '093361118', 'F3a7jN@yahoo.com', '!_9gY3#S5oKO'], ['Irwing', 'Velandia', '3352 85th street , 600', '11372', 'JACKSON HEIGHTS', '11', '25', '1978', '19172258338', 'NY', '078949097', 'dB3psGS@gmail.com', '&_8KZ5tbL$E9fSu'], ['Claudette', 'Morgan', '10208 Avenue J', '11236', 'Brooklyn', '08', '28', '1963', '19175395805', 'NY', '097666441', '6Oy2jCL91s@gmail.com', '5_32FT97ani4M'], ['Mohamed', 'Yatabarry', '1305 Sheridan avenue 3E', '10456', 'BRONX', '09', '15', '1980', '13476149880', 'NY', '095690576', 'sP4fg_r@yahoo.com', 'LBqC&lH#f3_w8i65m'], ['Liping', 'Chen', '967 46th Street', '11219', 'BROOKLYN', '10', '16', '1989', '19174705656', 'NY', '134963209', 'Kgql1X@hotmail.com', 'u#AESGUV&l37T'], ['Diane', 'Fiorello', '3218 shore road', '11572', 'Oceanside', '05', '22', '1971', '15165438260', 'NY', '073587067', 'HI5GZN_@yahoo.com', 'AR26#F837#g!M'], ['Bechir', 'Bejaoui', '364 93rd St Apt F4', '11209-6928', 'Brooklyn', '07', '25', '1974', '17182005710', 'NY', '082927470', 'iHVpu2Nn@yahoo.com', 'p6v!fUD#W5g_'], ['Carmen', 'Martinez', '201 Hufcut Road', '10941', 'MIDDLETOWN', '11', '28', '1969', '18453811877', 'NY', '437296304', 'e0f_EQVsOPIl@mail.com', '2ni8E7zS#DR'], ['Sean', 'Sliker', '6101B Scotch Pine Dr', '13603', 'Watertown', '12', '17', '1985', '18149691595', 'NY', '198702240', 'Cb2KX3JIkcts@gmail.com', '_s1dt7GoKz&84Z#l2$O9'], ['Iryna', 'Tamboutsava', '18 Bay 34th St Apt 3R', '11214', 'Brooklyn', '03', '07', '1971', '16316623304', 'NY', '079949480', 'BtM9HTOhc6@hotmail.com', 'uks&n2!g1rE@Yw'], ['Staffon', 'Donerlson', '139 Griffith st', '13208', 'SYRACUSE', '09', '19', '1984', '13154509789', 'NY', '061709441', 'VQxmjqv@hotmail.com', '059p7KL&EZzJV2!$Ne'], ['DAVID', 'CAICEDO', '1690 METROPOLITAN AVE APT 6E', '10462', 'Bronx', '10', '02', '1973', '13479906491', 'NY', '083920052', 'OLi3mEe8GDP@gmail.com', '09D&A63f7IjK'], ['Christopher', 'Joseph', '26 Satinwood Street', '11722', 'CENTRAL ISLIP', '11', '13', '1962', '16317414616', 'NY', '116601314', 'BUQ7coywKM6k@hotmail.com', 'gl@IZ5JR4_#Yz&69W8e'], ['Chinghua', 'Tang', '3351 84th St Apt 6E', '11372-1521', 'Flushing', '09', '26', '1951', '17184577515', 'NY', '017662034', '18wgtWCZoIv@yahoo.com', 'mN15B0lS##3@!'], ['Tracey', 'Fabiani', '100 Colfax Avenue', '10306', 'Staten Island', '02', '09', '1979', '19179512235', 'NY', '131646871', 'SQEMXg@mail.com', '!$7&DTv0sh65Nx#p2L8k'], ['Jennifer', 'Grant', '19807 116th ave',
    # '11412', 'SAINT ALBANS', '11', '18', '1974', '13472481167', 'NY', '116646302', '0O_SZh@gmail.com', 'YCIin$tG01L_#'], ['vincent', 'leone', '22 gettysburg dr', '11741', 'HOLBROOK', '02', '18', '1970', '13472348634', 'NY', '061487568', 'NpoULtu0@hotmail.com', '#Q@3kGA40Lj!MF'], ['Evelina', 'Cepeda', '565 W 139th St Apt 4', '10031', 'New York', '02', '09', '1971', '19292163416', 'NY', '054907741', 'M5OLgU7kvh81@hotmail.com', 'Bw4unX#S&!23$1'], ['Franco', 'DiMarino', '62 Fremont street', '10528', 'HARRISON', '04', '08', '1962', '19143643285', 'NY', '101649574', 'eJHM8o3uc@gmail.com', 'qup8423shC&J_f'], ['Brenda', 'Toney', '143 North 26th Street', '11798', 'Wyandanch', '04', '04', '1968', '16316712431', 'NY', '069586151', 'bTACrwF@mail.com', '#o&A$!80bGJlU31L'], ['Eric', 'Groberg', '1 Lincoln Plaza', '10023', 'New York', '03', '25', '1961', '19173597449', 'NY', '063467414', 'mOj0Sv@gmail.com', '1wF4f@#S37aN6'], ['Carter', 'Comden', '1801 Walker Lake Ontario Rd', '14468', 'Hilton', '07', '04', '1994', '15853697725', 'NY', '126824514', 'AmQhnBFUyL0@gmail.com', '@wi96TRWv3B8XO'], ['Gabrielle', 'Rivas', '2698 Creston Ave', '10468', 'BRONX', '01',
    # '15', '1991', '14079567492', 'NY', '082780106', 'avlSojp1PnED@yahoo.com', 'ONa#2BVx90qW'], ['Deborah', 'Dryden', 'PO Box 113', '13053-0113', 'Dryden', '10', '11', '1978', '16073454869', 'NY', '065649768', 'Cai_sEUZw@yahoo.com', '8#Fwj7sKmr0i'], ['Rayon', 'Richards', '25927  148th Road', '11422', 'Rosedale', '12', '19', '1982', '13478690609', 'NY', '055748395', '0ATk16Duoam2@hotmail.com', 'rw52c30#!N@a$dR9hJX'], ['NICOLE', 'DERBOGHOSSIAN', '28 SWENSON DR', '12590', 'Wappingers Falls', '03', '06', '1988', '19144383360', 'NY', '120764580', 'Pkpl1gVA@hotmail.com', '$I#7@26Tmln4#jpGy'], ['Stephen', 'Mateunas', '779 County Highway 41', '12155', 'Schenevus', '08', '11', '1979', '16072676865', 'NY', '123623799', 'kr6e_cMVoCi0@mail.com', 'd40gRHzl8#QC3'], ['Ivan', 'Velazquez', '123 Lafayette Ave Apt 3', '14213', 'Buffalo', '03', '22', '1997', '17165415123', 'NY', '596546843', 'Wg4vrxwF@gmail.com', 'xG$Qkeg60q!'], ['sonia', 'pozo', '905 tinton ave', '10456', 'BRONX', '12', '26', '1969', '19172599852', 'NY', '057687330', 'HXcV_d3Gi5R@hotmail.com', 'Rom!W$5Jz6YrN'], ['Melissa', 'Flores', '82 Columbus Ave', '11722', 'Central Islip', '01', '24', '1981', '16314359015', 'NY', '097668842', 'gjzJ_L@gmail.com', 'w1pPx#W9c@oTN_34&86y'], ['Michelle', 'Machuhovsky', '5532 Purdy Rd', '14424', 'CANANDAIGUA', '10', '11', '1966', '15856628084', 'NY', '080641917', 'GMyDi4V@gmail.com', 'BG6ry2Vt#k@Ld&x'], ['Casandra', 'Newsome', '965 Columbus Ave Apt 7B', '10025-3183', 'New York', '05', '07', '1973', '19175205227', 'NY', '133601915', 'f1J4spqAavm@gmail.com', '25t6pr&3vGz4'], ['Greg', 'Yerman', '563 Carlton Ave Apt 2', '11238', 'Brooklyn', '01', '28', '1963', '17182308646', 'NY', '591689028', 'RQ7Pmf8KG_zn@gmail.com', 'Y9B7T403bA_Q1'], ['LUIS', 'SINCHI', '49 CANDIDO AVE', '11967', 'SHIRLEY', '06', '07', '1985', '16312940526', 'NY', '064923888',
    # 'bUxA26XHgseZ@hotmail.com', '#R17P@Qt_Vx4'], ['Kyle', 'Keysor', '9 Hammond street', '12929', 'DANNEMORA', '03', '15', '1990', '15185930613', 'NY', '055785153', 'xwuSK73I@yahoo.com', 'ACH49q!er'], ['Baldev', 'Singh', '8906 Pontiac St 1st floor', '11427-2728', 'Queens Village', '11', '15', '1959', '17188647207', 'NY', '088829644', 'B1P6C0uqIF@gmail.com', '$7@gh42TwtOpjl'], ['Rafi', 'Hamif', '95 Krug Place', '11501', 'MINEOLA', '06', '05', '1958', '16319017073', 'NY', '060882462', 'kMfCPl4e@mail.com', '9YeGS#f5V_lvm#6!d347'], ['Cesar', 'Rodriguez', '450 e market st', '11561', 'LONG BEACH', '07', '12', '1978', '15164311646', 'NY', '088801405', 'fMGj_kcs@gmail.com', '83$FKs657DW2'], ['Krystal', 'Whaley', '798 Albany Avenue', '11203', 'BROOKLYN', '11', '28', '1991', '19176153367', 'NY', '064804581', '_DvW1JPX@yahoo.com', '!8V3KPq##pz'], ['Ezra', 'Turkel', '500 grand st B2A', '10002', 'New York', '12', '25', '1967', '19173347529', 'NY', '050489690', 'xbYZqQOERj@yahoo.com', 'S$RZ&p3@9aN5VcK'], ['Kisha', 'Gomez', '3225 Parkside Place #5F', '10467', 'BRONX', '11', '06', '1990', '13473751228', 'NY', '092788019', 'Vd1cYu4fA@gmail.com', 'iSy_Ytph01KCT5'], ['Amaury', 'Villalobos', '3101 park blvd', '10306', 'STATEN ISLAND', '01', '31', '1970', '16465153209', 'NY', '116566756', 'JDP_cn41VM@yahoo.com', 'j#hGb&u@5Czt7_']]
    # accList = accList = [
    #     ['Delia', 'Nelson', '3966  Fire Access Road', '27406', 'Greensboro', '12', '13', '1993', '336-971-4043', 'NC',
    #      '684-09-4509', 'rNMGTY@gmail.com', 'n_Dy2Oxajt4'],
    #     ['Kristen', 'Segura', '4089  Morris Street', '78021', 'Fowlerton', '3', '19', '1994', '830-373-0755', 'TX',
    #      '627-48-2639', '1mfpMH05xz@gmail.com', '73Yqs9@u!5b'],
    #     ['Willie', 'Haskins', '1489  Dog Hill Lane', '66418', 'Delia', '12', '5', '1993', '785-771-5043', 'KS',
    #      '511-64-4047', 'XIZRue@hotmail.com', 'fMRCDJ8@U0G#P'],
    #     ['Diana', 'Straight', '2967  Hillcrest Lane', '90017', 'Los Angeles', '12', '15', '1993', '949-860-5244', 'CA',
    #      '573-47-1737', 'FKJEdY7Nlm@yahoo.com', 'Fx8m34IT59Z#i7'],
    #     ['Timothy', 'Putman', '4450  Bobcat Drive', '21701', 'Frederick', '9', '21', '1993', '240-920-4782', 'MD',
    #      '214-39-6557', 'j3_duNxGMn9a@yahoo.com', 'c4&A9#POF8M$N_m'],
    #     ['Joseph', 'Norris', '1402  Twin Oaks Drive', '49770', 'Petoskey', '1', '18', '1994', '231-439-9382', 'MI',
    #      '377-74-3309', '71lgNYdf@gmail.com', '#S2Vg_@yH1'],
    #     ['Natividad', 'Devaughn', '4897  Sugarfoot Lane', '47904', 'Lafayette', '7', '15', '1994', '765-447-4915', 'IN',
    #      '308-38-2333', 'y7gdNO3@mail.com', 'OV4E@ij2U6G!#sS5&'],
    #     ['Melanie', 'Anderson', '4243  Buck Drive', '84118', 'Kearns', '9', '8', '1993', '801-964-0701', 'UT',
    #      '646-74-5616', 'jIklgQ@mail.com', 'NETHLn$#h9@0it8!'],
    #     ['Irina', 'Morison', '1526  Sycamore Fork Road', '33176', 'Miami', '12', '21', '1993', '954-224-6800', 'FL',
    #      '771-18-3573', '7VdopKUG@hotmail.com', 'UE!9$t6#8MI432v_P'],
    #     ['Emma', 'Roberts', '1879  Glendale Avenue', '90040', 'City Of Commerce', '10', '17', '1993',
    #      '818-681-1110', 'CA', '563-47-1908', 'YexXsJqoTaZB@yahoo.com', '2#DW45csHM1yETQ9'],
    #     ['Matthew', 'Coffman', '2213  Poplar Lane', '33139', 'Miami', '2', '7', '1994', '305-531-5453', 'FL',
    #      '595-21-2285', '9AicSwpN@yahoo.com', 'Sx40L3eI8o5Bg!'],
    #     ['David', 'Underwood', '1246  Alpaca Way', '92614', 'Irvine', '7', '9', '1994', '714-675-9331', 'CA',
    #      '562-96-6029', 'aOuqLn@mail.com', 'B5oKb4Y#FSI9O0!'],
    #     ['Ronald', 'Larson', '4753  Nelm Street', '22070', 'Herndon', '12', '25', '1993', '571-749-1310', 'VA',
    #      '229-45-6437', 'OjWeviS9@gmail.com', '50mMYr489tNz1O$V#'],
    #     ['Jonathon', 'Carter', '4763  Stewart Street', '46204', 'Indianapolis', '10', '2', '1993', '317-637-5216', 'IN',
    #      '308-26-1474', '5RW7KbI@yahoo.com', '_A4$0C36qUi7'],
    #     ['Michael', 'Byrd', '3366  Goldleaf Lane', '7304', 'Jersey City', '7', '23', '1994', '201-600-5370', 'NJ',
    #      '147-44-6559', 'Xcs4wPxtA@hotmail.com', 'E8$6HXAD#P0uj'],
    #     ['Christina', 'Burnham', '4549  Meadow Lane', '94612', 'Oakland', '9', '26', '1993', '707-289-5624', 'CA',
    #      '547-05-6033', 'bP2wo6amW3@gmail.com', '716t#vF#8yQ$'],
    #     ['John', 'Bowles', '489  Half and Half Drive', '93721', 'Fresno', '9', '1', '1993', '559-904-9942', 'CA',
    #      '565-46-3013', 'AVFkUb@gmail.com', 'C_8!$DNPWV0@'],
    #     ['Antonio', 'Gibson', '1202  Brannon Street', '90017', 'Los Angeles', '5', '7', '1994', '213-225-8861', 'CA',
    #      '547-42-8008', 'nOw86cXdfMG@hotmail.com', '#Wi#1l8RLX'],
    #     ['Erika', 'Fremont', '2666  Valley Drive', '19103', 'Philadelphia', '9', '22', '1993', '267-352-5846', 'PA',
    #      '201-18-3212', 'jk1H_X6@yahoo.com', '5072Juv4iT#6e!BD#'],
    #     ['Dorothea', 'Flowers', '709  Richland Avenue', '77063', 'Houston', '11', '8', '1993', '281-271-3513', 'TX',
    #      '463-80-8276', 'rXt0zkYL5@hotmail.com', 'O3#7UKQx6D0w_NX&54V'],
    #     ['Margaret', 'Adkins', '2025  Kelley Road', '39520', 'Bay St Louis', '2', '22',
    #      '1994', '228-466-2247', 'MS', '428-16-0565', 'jAw5cJXfH@gmail.com', '4$@se5OR3#8&0g'],
    #     ['Jamie', 'Fullerton', '1902  Stonepot Road', '7477', 'Wayne', '10', '14', '1993', '908-338-9147', 'NJ',
    #      '141-28-6245', '94fqvOzk7_l3@yahoo.com', 'U_@$3#hJpNTC4e'],
    #     ['Louisa', 'Hayes', '155  Carriage Lane', '17815', 'Bloomsburg', '5', '12', '1994', '570-242-7405', 'PA',
    #      '176-07-1473', '1ky4mu@gmail.com', 'En&6$aO9Z_!'],
    #     ['Grace', 'Park', '2542  Mutton Town Road', '98382', 'Sequim', '9', '12', '1993', '360-683-0753', 'WA',
    #      '538-50-3315', 'gsDbidX@yahoo.com', 'syb13K2I#@4D#Rvt'],
    #     ['Carol', 'Cullen', '2009  Blane Street', '63101', 'Stlouis', '1', '8', '1994', '314-578-9764', 'MO',
    #      '489-46-0207', '_XmW45ECQv8@hotmail.com', '_#9Qm835eD6j&7'],
    #     ['Theresa', 'Dubuc', '317  Hickory Heights Drive', '21202', 'Baltimore', '12', '19', '1993', '443-851-9129',
    #      'MD', '213-74-4084', 'QGsctPhqb2va@mail.com', 'p_Sn3xj6u$m#&'],
    #     ['Sheila', 'Armstrong', '3304  Public Works Drive', '37756', 'Huntsville', '9', '8', '1993', '423-319-0110',
    #      'TN', '763-01-0463', 'h2fw9xVecao@mail.com', '5#0I#BklgR4iaNV_'],
    #     ['Ann', 'Dewberry', '4450  Rockwell Lane', '27834', 'Greenville', '5', '10', '1994', '252-578-3293', 'NC',
    #      '239-39-6266', 'rfvECkzMDI@gmail.com', 'WyjTrZ1#Hidb2'],
    #     ['Carol', 'McClellan', '3235  Patterson Road', '11208', 'Brooklyn', '12', '1', '1993', '718-827-6889', 'NY',
    #      '074-09-1803', '5S0mLC1RrZt@gmail.com', '#hy_QSD23509$re'],
    #     ['Mary', 'Walker', '3699  Winifred Way', '46135', 'Greencastle', '12', '7', '1993', '765-721-2342', 'IN',
    #      '313-70-8572', 'Zg45QvdC@mail.com', '1Ndp&La0S#5'],
    #     ['Dorothy', 'Tighe', '4138  Flanigan Oaks Drive', '20720', 'Bowie', '8', '11', '1994', '301-352-0644', 'MD',
    #      '213-46-2998', 'S_54NsdCbLE@yahoo.com', '1REG@Jsub#!L9F6'],
    #     ['Charlotte', 'Darnall', '4874  James Avenue', '67114', 'Newton', '9', '7', '1993', '316-283-6964', 'KS',
    #      '511-08-9818', 'bLXc6p@hotmail.com', '67@$9S1vlVn5xq'],
    #     ['Tina', 'Doyle', '661  Kooter Lane', '28208', 'Charlotte', '9', '23', '1993', '704-395-4116', 'NC',
    #      '688-01-6266', 'Zfd3tuwa@yahoo.com', '42o#8F!3ywE5N0$'],
    #     ['Michael', 'Martin', '725  Sussex Court', '76541', 'Killeen', '7', '21', '1994', '254-466-6131', 'TX',
    #      '453-71-6105', 'yNKiIg_C7kVP@mail.com', 'VI71yA823oJ6gk_'],
    #     ['Joanna', 'Schwager', '692  Sugar Camp Road', '56297', 'Wood Lake', '12', '19', '1993', '507-485-7848', 'MN',
    #      '477-22-9215', 'AxnmM9u@hotmail.com', '6Hd$m7p4XJ285#aB'],
    #     ['Tyrone', 'Boyland', '2264  Dennison Street', '95202', 'Stockton', '8', '17', '1994', '209-587-7462', 'CA',
    #      '606-13-0714', 'c714tVT8bs@hotmail.com', '!4MrsP7F$'],
    #     ['Theresa', 'McKay', '1771  Harter Street', '45133', 'Sinking Spring', '10', '23', '1993', '937-588-6044', 'OH',
    #      '275-11-6931', 'ov6kYdBL7Gz@yahoo.com', '4#A$DNLi5BeG#'],
    #     ['Ellen', 'Taylor', '3537  Fidler Drive', '78217', 'San Antonio', '8', '28', '1993', '210-723-5585', 'TX',
    #      '453-42-4552', 'C7KN61uT@yahoo.com', 'z9LmT83Iv!1'],
    #     ['Paul', 'Whiddon', '2578  Beech Street', '94585', 'Sunol', '10', '17', '1993', '925-862-9457', 'CA',
    #      '617-06-9973', 'oUXYuKDBR@gmail.com', 'R!2ngM9Q'],
    #     ['Billy', 'Franklin', '728  Blane Street', '63101', 'Stlouis', '5', '16', '1994', '314-619-3331', 'MO',
    #      '493-03-3824', 'VZEmuQs@yahoo.com', '40rQw$gI8!Ka_71'],
    #     ['Ned', 'Shockley', '813  Broaddus Avenue', '42701', 'Elizabethtown', '8', '7', '1994', '270-260-8096', 'KY',
    #      '403-05-5002', 'GV9PFDJwY@mail.com', 'a!@4RWbg2'],
    #     ['Jorge', 'Rollins', '4470  Jerry Dove Drive', '29501', 'Florence', '4', '22', '1994', '843-432-6161', 'SC',
    #      '250-67-4939', 'TeuY8c@yahoo.com', 'ae7Hf0rp#d'],
    #     ['Carmen', 'Browder', '3163  Arbutus Drive', '33166', 'Miami Springs', '10',
    #      '4', '1993', '305-870-7422', 'FL', '590-66-3917', 'zHObIxs@mail.com', 'FU19@d26oGbI#5#D$Z'],
    #     ['Victoria', 'Duffy', '4434  Patterson Road', '11219', 'Brooklyn', '8', '24', '1994', '718-871-3560', 'NY',
    #      '072-54-9473', 'oLk1bFBG_@gmail.com', '104IS5$Nxfc2&A#8'],
    #     ['Carol', 'Williams', '2178  Musgrave Street', '73102', 'Oklahoma City', '2', '16', '1994', '405-241-9247',
    #      'OK', '443-24-6748', 'FCht7v_A@mail.com', 'c0r!m43n&#9wzf'],
    #     ['Gladys', 'Mishler', '3918  College Avenue', '45326', 'Fletcher', '6', '6', '1994', '937-368-9922', 'OH',
    #      '298-08-7462', 'Ys4kPnuj@gmail.com', '1DfI9#236FJ#'],
    #     ['Darlene', 'Allman', '1316  Asylum Avenue', '10583', 'Scarsdale', '5', '3', '1994',
    #      '203-726-1462', 'CT', '044-92-7882', 'ZKEb1UF2@yahoo.com', '7@5#C&nXBw2T'],
    #     ['Violet', 'Babb', '1884  Lake Forest Drive', '10549', 'Mount Kisco', '9', '21', '1993', '914-242-6845', 'NY',
    #      '051-44-1498', '8M6VeDnp3Q@mail.com',
    #      '#y0#2vYp7uBg8o6U9'],
    #     ['Esther', 'Suzuki', '2118  Sugar Camp Road', '55060', 'Owatonna', '11', '28', '1993', '507-539-8977', 'MN',
    #      '471-70-3369', 'XNoKBtIVkEFu@hotmail.com', 'X&0_ywuYG1@bT'],
    #     ['Angela', 'Johnson', '251  Buck Drive', '5153', 'Proctorsville', '12', '11', '1993', '802-226-3344', 'VT',
    #      '009-24-6211', 'DSk_fWLEcF@hotmail.com', '_Gt6zbC#MV5d'],
    #     ['Esther', 'Dunn', '217  Fannie Street', '77803', 'Bryan', '1', '6', '1994', '979-200-9997', 'TX',
    #      '627-38-0985', '0Y86lyMjf@hotmail.com', 'DXBAEJs7$9'],
    #     ['Diane', 'Juarez', '4431  Collins Street', '16920', 'Elkland', '3', '10', '1994', '814-258-5949', 'PA',
    #      '196-62-7446', '5oGTEzQ2PfX@gmail.com', 'IB0&_lUK9k87$3tW2'],
    #     ['Misty', 'Maxfield', '1381  Lawman Avenue', '22206', 'Arlington', '9', '8', '1993', '703-305-2104', 'VA',
    #      '228-09-0302', 'ncSNv_6yzo@hotmail.com', 'x#Dy#iBw!8@A03h6W9t'],
    #     ['Robert', 'Stovall', '5034  Filbert Street', '19034', 'Fort Washington', '1', '17', '1994', '610-801-1009',
    #      'PA', '169-44-0689', '7L2laUTGvS@gmail.com', 'c!uCQP_kW2RD0'],
    #     ['Joseph', 'Hudson', '2066  Burwell Heights Road', '77002', 'Houston', '4', '13', '1994', '409-440-7083', 'TX',
    #      '636-09-4964', 'HBUawSAOv@hotmail.com', 'B!#0_6Kznw9&lX'],
    #     ['Scottie', 'Payne', '4121  Rockford Road', '89317', 'Lund', '6', '4', '1994', '775-238-1744', 'NV',
    #      '680-12-8628', 'c3ZMos2H@gmail.com', 'tV1!fOR7&#Puv9@b63'],
    #     ['John', 'Medellin', '1357  Elm Drive', '10013', 'New York', '4', '7', '1994', '646-479-8889', 'NY',
    #      '065-40-4254', '1fvyDeu_nd@gmail.com', 'Do20pz3S#$4!@Rc'],
    #     ['Maria', 'Long', '2531  Centennial Farm Road', '51231', 'Archer', '11', '15', '1993', '712-723-1742', 'IA',
    #      '480-08-1915', 'ZwgMAKv35c@hotmail.com', 'ZKNC$6gS3L51Hv92'],
    #     ['John', 'Lewis', '591  Eva Pearl Street', '70810', 'Baton Rouge', '2', '26', '1994', '225-766-5639', 'LA',
    #      '662-07-3639', 'cXD_6s7l3Lwj@mail.com', '1$aK8dG3@pXOv'],
    #     ['Michael', 'Nelson', '3517  Court Street', '63132', 'Olivette', '2', '26', '1994', '636-674-0176', 'MO',
    #      '489-62-1371', '2vVNk8l@yahoo.com', 'uF&125oZJ38#EQ'],
    #     ['Thomas', 'Ryan', '1933  Heliport Loop', '47201', 'Columbus', '1', '3', '1994', '812-707-2475', 'IN',
    #      '315-94-1572', 't5KYdMmi7XL2@mail.com', '&bF2ua675l1'],
    #     ['Thaddeus', 'Reinhart', '280  Gnatty Creek Road', '11590', 'Westbury', '6', '20', '1994', '516-408-4373', 'NY',
    #      '071-38-5383', 'c2WJiD9d@yahoo.com', '8cmB&Ja@#u47'],
    #     ['Steven', 'Jones', '2717  Coal Street', '15904', 'Johnstown', '11', '12', '1993', '814-330-9740', 'PA',
    #      '207-66-2816', 'bdV5NmGa3O@mail.com', 'j6V!Rb5rHeaOI'],
    #     ['Hung', 'Flinchum', '2012  Queens Lane', '24501', 'Lynchburg', '7', '31', '1994', '434-841-5405', 'VA',
    #      '224-19-6993', '65KVe3W1O@mail.com', 'O51@!RI#D#PM'],
    #     ['William', 'Musial', '3002  Bassel Street', '70301', 'Thibodaux', '2', '16', '1994', '985-449-2369', 'LA',
    #      '663-09-6457', 'VFGCam@hotmail.com', 'D&A#bJo7250n3w8H'],
    #     ['Edward', 'McCauley', '1386  Simpson Street', '61264', 'Milan', '12', '20', '1993', '309-756-5645', 'IL',
    #      '322-44-3035', 'w3W0lQ6uvp@hotmail.com', 'X2uDh@84Bdc#31'],
    #     ['Julie', 'Danford', '632  Sugarfoot Lane', '46901', 'Kokomo', '8', '7', '1994', '765-457-8199', 'IN',
    #      '315-04-4989', '_EcrwMOet4oa@hotmail.com', '#!f4&@LVyWnz6'],
    #     ['Megan', 'Adams', '545  Gore Street', '77027', 'Houston', '10', '27', '1993', '713-590-6239', 'TX',
    #      '456-14-2953', 'MF7fpYKZ@mail.com', '#ju_0la#74K&'],
    #     ['Bernice', 'Monroe', '2030  Saint Francis Way', '53005', 'Brookfield', '1', '6', '1994', '262-989-5781', 'WI',
    #      '392-04-7984', '8sQ7V2qgGOjI@hotmail.com', '8U1O@0346!sqBy'],
    #     ['Franklyn', 'Pence', '2394  Norma Lane', '71302', 'Alexandria', '12', '22', '1993', '318-496-0760', 'LA',
    #      '661-03-2342', 'djBcT_3ECfI@gmail.com', 'd4g0#xjpvK$Pcb'],
    #     ['Patricia', 'Noone', '4001  Walnut Street', '39654', 'Monticello', '2', '4', '1994', '601-587-2647', 'MS',
    #      '427-60-0975', 'q_NzIUl2c0@mail.com', 'IEf15Pdq9027_'],
    #     ['John', 'Walker', '624  Courtright Street', '58801', 'Williston', '11', '15', '1993', '701-577-2526', 'ND',
    #      '501-11-1699', 'xfeRHDEUbLV@gmail.com', 'ef&57q@!id'],
    #     ['Anna', 'Myers', '4492  Marshville Road', '10641', 'White Plains', '6', '8', '1994', '845-603-6066', 'NY',
    #      '113-14-9423', '_WFd0n1e@hotmail.com', 'OoTF7x8z064@L$Jy'],
    #     ['Mary', 'Baker', '3296  Rubaiyat Road', '49503', 'Grand Rapids', '8', '5', '1994', '231-672-2197', 'MI',
    #      '378-24-6982', 'AuQhWZE_s2Bp@gmail.com', '01p_l4UALuvR5'],
    #     ['Timothy', 'Tucker', '4234  Northwest Boulevard', '7662', 'Rochelle Park', '2', '23', '1994', '201-924-7773',
    #      'NJ', '148-06-7101', 'aPX1tZiRW@mail.com', '1u_20#6m3$r7fih'],
    #     ['Daniel', 'Lopez', '1670  Brighton Circle Road', '56345', 'Little Falls', '10', '17', '1993', '320-630-9101',
    #      'MN', '477-66-2043', '6YRJEa7dlM@gmail.com', '0SHLZuYA2@#$1eO7&'],
    #     ['Sherry', 'Jacobs', '4454  Pin Oak Drive', '90815', 'Long Beach', '1', '20', '1994', '562-985-0640', 'CA',
    #      '568-33-0785', 'ABcfIPMCz@yahoo.com', '59#3rjuJY0Zb7P'],
    #     ['Lucy', 'Phillips', '4387  Farland Avenue', '78229', 'San Antonio', '9', '11', '1993', '830-577-3916', 'TX',
    #      '644-32-5872', 'Qf4a0wN@yahoo.com', 'Ql9!c1U2Nsbf&_'],
    #     ['Joshua', 'Lefkowitz', '2773  Owagner Lane', '98109', 'Seattle', '12', '8', '1993', '206-251-3522', 'WA',
    #      '539-19-9598', '_cFdIP@mail.com', 'M526GS3QK87#hPqWa'],
    #     ['Joaquin', 'Santamaria', '47  Columbia Road', '19720', 'Wrangle Hill', '12', '25', '1993', '302-832-7048',
    #      'DE', '222-30-4369', 'E7sBcMAF13@hotmail.com', 'd$0Z59_2XJn#z86&'],
    #     ['Noah', 'Conway', '3120  Marigold Lane', '33169', 'Miami', '7', '17', '1994', '305-404-3592', 'FL',
    #      '595-87-7848', 'WIZoimh@mail.com', 'AZwi&t$rS273C84#R9'],
    #     ['Scott', 'Major', '1763  Raintree Boulevard', '55372', 'Prior Lake', '8', '17', '1994', '763-746-7546', 'MN',
    #      '471-18-3857', '_iSF9QRw@gmail.com', 'i2P7nSlO!Y'],
    #     ['James', 'Ortiz', '1861  Garrett Street', '18101', 'Allentown', '9', '8', '1993', '267-999-5677', 'PA',
    #      '204-50-3731', 'FZWR2hDA@yahoo.com', 'tQ@Y2Zvl1p'],
    #     ['Justin', 'Arroyo', '231  Union Street', '98121', 'Seattle', '4', '29', '1994', '206-770-4765', 'WA',
    #      '531-22-8991', 'WvXBx2sp@gmail.com', '_nd!bT9$364uMkw&'],
    #     ['John', 'Brown', '1195  Grove Street', '11714', 'Bethpage', '8', '19', '1994', '631-801-5361', 'NY',
    #      '112-10-8635', 'YVOyZ42_f@mail.com', 'n14hj37kL&9N5m'],
    #     ['Lynn', 'Leflore', '1932  Finwood Road', '8872', 'Sayreville', '9', '29', '1993', '732-523-1111', 'NJ',
    #      '152-18-3037', 'kTCID1zPB@yahoo.com', '7#59t40hgHWU_V$6I'],
    #     ['Cara', 'Pehrson', '2102  Cedar Lane', '2115', 'Boston', '12', '24', '1993', '617-638-5740', 'MA',
    #      '029-48-7528', 'j0mvGTFIt@mail.com', '2$9VztmRHxi#u#B'],
    #     ['Marsha', 'Aviles', '3839  Viking Drive', '45732', 'Glouster', '8', '18', '1994', '740-767-0017', 'OH',
    #      '273-98-5463', 'a62e0zvgP5F@hotmail.com', 'l3O5&UXmKuH68x'],
    #     ['Joseph', 'Logan', '1935  White River Way', '84020', 'Draper', '10', '22', '1993', '801-553-8149', 'UT',
    #      '647-05-2988', 'hNm2tq@yahoo.com', '6K4Cc51b#qFgRMx'],
    #     ['Albert', 'Spinks', '4140  Nutters Barn Lane', '50317', 'Des Moines', '11', '21', '1993', '515-645-3155', 'IA',
    #      '482-86-5434', 'e3N4FLmw@yahoo.com', '1!x3qU5H4u26'],
    #     ['Amanda', 'Hill', '2435  Riverwood Drive', '95926', 'Chico', '5', '7', '1994', '530-380-8941', 'CA',
    #      '569-49-1101', 'S5Iwpjaq6Qr@hotmail.com', 'V8xPBF@KI95#&TS72'],
    #     ['Shirley', 'Schuette', '1686  Cottonwood Lane', '49503', 'Grand Rapids', '11', '16', '1993', '616-347-8817',
    #      'MI', '374-14-6627', 'XRZj6FBtdSJ@hotmail.com', '#B9OIL!$VP#C4'],
    #     ['William', 'Gladden', '2618  Glen Street', '42041', 'Fulton', '1', '20', '1994', '270-370-4088', 'KY',
    #      '407-09-4546', 'iZhQ7OXaefHc@mail.com', '$!r@JSobcfX97'],
    #     ['Lester', 'Brown', '4852  Nutter Street', '64127', 'Kansas City', '9', '25', '1993', '816-242-4155', 'MO',
    #      '489-15-9312', 'zRm3wsf1n5G_@mail.com', 'Q#F0R!DVC946&2H'],
    #     ['Myrtice', 'Draper', '2860  Grant View Drive', '53150', 'Muskego', '4', '30', '1994', '414-422-5796', 'WI',
    #      '394-07-0071', 'YTwViL@mail.com', 'vKYTzCe$691'],
    #     ['Marshall', 'Smith', '2050  Atha Drive', '93311', 'Bakersfield', '11', '6', '1993', '661-665-1511', 'CA',
    #      '554-70-9595', '4UcDJqVj@yahoo.com', 'pKY#I7S805!&2'],
    #     ['Marie', 'Reed', '135  Rainbow Drive', '44286', 'Richfield', '1', '6', '1994', '330-523-3763', 'OH',
    #      '278-48-8651', '4pTSCwH@hotmail.com', 'u7Rh@_aop8$y#r45'],
    #     ['Brenda', 'Murray', '257  John Calvin Drive', '60523', 'Oak Brook', '8', '6', '1994', '708-925-4875', 'IL',
    #      '325-04-1877', '8aFRel@mail.com', 'nlr37Mi#e_'],
    #     ['Elizabeth', 'Saunders', '581  Valley Street', '8108', 'Collingswood', '3', '29', '1994', '856-858-2128', 'NJ',
    #      '136-07-1214', 'NFpLtBei_aQ@gmail.com', '7Mw#6&dogAps!Nq'],
    #     ['James', 'Vaughn', '2061  Rainy Day Drive', '2127', 'South Boston', '6', '4', '1994', '617-981-0608', 'MA',
    #      '034-48-1052', 'lE8TvpdY@hotmail.com', 'z!NqcPKiRt@489#w76'],
    #     ['Donald', 'Anderson', '430  Edwards Street', '27834', 'Greenville', '9', '30', '1993', '252-717-5294', 'NC',
    #      '685-07-8977', 'BECcGmk_rH@yahoo.com', '_@EN&HMY6U1nS']]
    # print(change_bank_account())
    # count = 0
    # currentLine = 59
    # # 更换ip次数
    # globalCount = 6
    # for item in accList[59:79]:
    #     if count >= globalCount:
    #         count = 0
    #         # 执行超过6，切换代理
    #         AutoChangeProxy().change_ip(country="CA", ip="68.*.*.*")
    #         time.sleep(5)
    #     currentLine = currentLine + 1
    #     ins = Register(webUrl, item)
    #     print(item)
    #     print(ins.errorList)
    #     print(currentLine)
    #     ins.play()
    #     count = count + 1
    #     # if len(ins.errorList) > 0:
    #     #     AccountErrorSingleRecord([item])
    # print('currentLine')
    # print(currentLine)
    # print('错误列表')  
    # print(errorList)  
    # AccountErrorRecord(errorList)
    # AccountRecordSuccess(successList)
