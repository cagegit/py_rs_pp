from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from log import logger

numStr = '0123456789'
currentLine = 0
'''
 模拟注册类
'''


class LoginAndSign:
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
    def __init__(self, u_l_name, u_f_name, u_street, u_state, u_zip, u_c_name, u_c_pwd, sign_url, gift_url):
        self.errorList = []
        self.successList = []
        self.url = ''
        self.account = [u_l_name, u_f_name, u_street, u_state, u_zip, u_c_name, u_c_pwd]
        self.retryCount = 0
        self.u_name = u_c_name
        self.u_pwd = u_c_pwd
        # self.u_birth_day = u_birth_day
        # self.u_safe_code = u_safe_code
        # self.u_pay_account = u_pay_account
        self.sign_url = sign_url
        self.gift_url = gift_url
        #  总览页面
        self.summary_url = 'https://www.paypal.com/myaccount/summary?intl=0'
        #  付款页面
        self.transfer_url = 'https://www.paypal.com/myaccount/transfer/homepage'
        # 错误类型未知错误 => 1, 超时 => 2, 领券成功未支付 => 3
        self.error_type = '2'
        self.error_info = ''
        self.lq_success_list = []
        # self.userName = uName
        # self.passWord = uPass
        # logger.info(acccout)
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

    def play(self):
        # webdriver.Chrome(driver, options=)
        driver_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'driver',
                                   'chromedriver.exe')
        logger.info('let go!')
        logger.info(driver_path)
        self.driver = webdriver.Chrome(executable_path=driver_path, options=self.options)
        # self.driver.get(self.url)
        try:
            self.driver.get(self.sign_url)
            # time.sleep(10)
            nextBtn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'btnNext'))
            )
            if nextBtn:
                userNameInput = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'email'))
                )
                time.sleep(6)
                userNameInput.send_keys(self.u_name)
                nextBtn.click()
                passWordInput = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'password'))
                )
                time.sleep(6)
                passWordInput.send_keys(self.u_pwd)
            else:
                userNameInput = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'email'))
                )
                passWordInput = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'password'))
                )
                time.sleep(5)
                userNameInput.send_keys(self.u_name)
                time.sleep(5)
                passWordInput.send_keys(self.u_pwd)

            # 获取登录按钮
            submit_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.ID, 'btnLogin'))
            )
            # 点击登录按钮
            # time.sleep(1)
            submit_btn.click()
            time.sleep(5)
            # self.pay_to_account()
            try:
                receive_btn = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'myaccount-button'))
                )
                logger.info(receive_btn)
                logger.info('成功登录到指定页面！')
                self.ling_quan()
            except TimeoutException:
                logger.error('没有登录到指定页面！', exc_info=True)
                self.error_type = '2'
                self.error_info = '操作超时！没有登录到指定页面!'
            finally:
                logger.info('领券流程结束！')

            # time.sleep(200)
        except TimeoutException:
            logger.error('操作超时！该条数据可以重新使用', exc_info=True)
            self.error_type = '2'
            self.error_info = '操作超时！该条数据可以重新使用'
            self.errorList.append(self.u_name)
        except Exception as e:
            print(e)
            self.error_type = '2'
            self.error_info = '未知错误！该条数据可以重新使用'
            logger.error('未知错误！', exc_info=True)
            self.errorList.append(self.u_name)
        finally:
            print('全部流程完毕！')
            # time.sleep(10)
            self.driver.quit()
            # 验证码重试三次

    def ling_quan(self):
        self.driver.get(self.gift_url)
        time.sleep(5)
        # self.first_step()

        # 获取提示文本内容
        info_hero = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'p.info-hero__paragraph'))
            # EC.element_to_be_clickable((By.CSS_SELECTOR, 'p.info-hero__paragraph'))
        )
        # print(info_hero)
        logger.info(info_hero.get_attribute('textContent'))
        info_hero_text = info_hero.get_attribute('textContent')
        # 'You may have claimed' in str
        # if 'successfully claimed your offer' in info_hero_text:
        if 'you should receive your £5' in info_hero_text:
            # 领券成功
            logger.info('领券成功！')
            # self.error_type = '3'
            # self.lq_success_list = self.account
            self.successList.append(self.account)
            # 跳转到总览页面
            # self.driver.get(self.summary_url)
            time.sleep(3)
            #  判断接受款项按钮是否存在
            # a.ppvx_btn.ppvx_btn--inverse
            # self.accept_five()
        else:
            self.errorList.append(self.u_name)
            self.error_type = '1'
            self.error_info = '领券失败！'
            logger.error('没有购物券，领券失败，退出流程！')


# if __name__ == '__main__':
    # 登录链接
    # sign_url = 'https://www.paypal.com/signin/authorize?client_id=AWGB1KL2xHGOo453DgRGVYSb0M0wrFjRIMY6WCRkmdEZ6WqjjnAfnLOv3Rigupp5RoDr1wqBNHHtbSto&response_type=code&state=eyJmbG93X2lkIjoiMiIsInByb21vX2NvZGUiOiJQU0lfTFAwNiIsInJldHVybl91cmkiOiJodHRwczovL3d3dy5wYXlwYWwuY29tIiwiRURQIjoia0JWWmN5emlDSHNYY3RPZ0c2S0tnQT09In0=&redirect_uri=https://apply.syf.com/applylanding/ApplyLanding'
    # 领券链接
    # gift_url = 'https://www.paypal.com/uk/webapps/mpp/pfs/welcome/offer/mobile/5'
    # https://www.paypal.com/myaccount/transfer/homepage
    # fn-sendRecipient
    # button[type=submit]

    # 用户名、密码
    # u_name = '3437a7f@gmail.com'
    # u_pwd = '@As541287'
    # u_birth_day = '1978/7/31'
    # u_safe_code = '505237351'
    # u_pay_account = 'Patriciaedwardsibl8493@mail.ru'
    # u_name = '7849604@gmail.com'
    # u_pwd = '@As538709'
    # u_birth_day = '1929/1/9'
    # u_safe_code = '513241690'
    # u_pay_account = 'vdegyh@163.com'
    #
    # logAndSignIns = LoginAndSign(u_name, u_pwd, u_birth_day, u_safe_code, u_pay_account, sign_url, gift_url)
    # logAndSignIns.play()
