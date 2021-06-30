from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import os
from log import logger

numStr = '0123456789'
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
    def __init__(self, u_name, u_pwd, u_birth_day, u_safe_code, u_pay_account, sign_url, gift_url):
        self.errorList = []
        self.successList = []
        self.url = ''
        self.account = [u_name, u_pwd, u_birth_day, u_safe_code, u_pay_account]
        self.retryCount = 0
        self.u_name = u_name
        self.u_pwd = u_pwd
        self.u_birth_day = u_birth_day
        self.u_safe_code = u_safe_code
        self.u_pay_account = u_pay_account
        self.sign_url = sign_url
        self.gift_url = gift_url
        #  总览页面
        self.summary_url = 'https://www.paypal.com/myaccount/summary?intl=0'
        #  付款页面
        self.transfer_url = 'https://www.paypal.com/myaccount/transfer/homepage'
        # 错误类型未知错误 => 1, 超时 => 2, 领券成功未支付 => 3， 填写错误 =4 ,填写正确打款失败=5，transferMoney按钮存在，打款失败
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
            has_q_btn = False
            try:
                receive_btn = WebDriverWait(self.driver, 8).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'a.ppvx_btn.ppvx_btn--inverse'))
                )
                print(receive_btn)
                logger.info('接受款项按钮存在')
                has_q_btn = True
                # time.sleep(10000)
                self.accept_five()
            except TimeoutException:
                # 增加对余额的判断
                try:
                    transfer_money_a = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'a.test_balance_btn-transferMoney'))
                    )
                    print(transfer_money_a)
                    logger.info('transferMoney按钮存在')
                    has_q_btn = True
                    try:
                        self.pay_to_account()
                    except Exception as e:
                        print(e)
                        logger.error('打款未成功！', exc_info=True)
                        self.error_type = '6'
                        self.error_info = 'transferMoney存在,打款失败'
                except TimeoutException:
                    logger.info('transferMoney按钮不存在！')
                logger.error('没有接受按钮存在！', exc_info=True)
                # a.test_balance_btn - transferMoney
                if not has_q_btn:
                    self.error_type = '1'
                    self.error_info = '没有券存在'
                try:
                    ai_check = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.ID, 'ads-plugin'))
                    )
                    logger.info(ai_check)
                    if ai_check:
                        # 出现安全验证
                        self.error_type = '1'
                        self.error_info = '出现人机验证'
                        self.errorList.append('出现人机验证！')
                except Exception as e:
                    print(e)
                    logger.error('没有人机验证', exc_info=True)
            finally:
                logger.info('领券流程结束！')

            # time.sleep(200)
        except TimeoutException:
            logger.error('操作超时！该条数据可以重新使用', exc_info=True)
            # 增加安全验证判断
            has_ai_error = False
            logger.info('人机验证判断开始：')
            try:
                # ads-plugin
                ai_check = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.ID, 'ads-plugin'))
                )
                logger.info(ai_check)
                if ai_check:
                    has_ai_error = True
                    # 出现安全验证
                    self.error_type = '1'
                    self.error_info = '出现人机验证'
                    self.errorList.append('出现人机验证！')
            except Exception as e:
                print(e)
                logger.error('没有安全验证', exc_info=True)
            if not has_ai_error:
                if self.error_type == '3':
                    print('领券成功！')
                else:
                    self.error_type = '2'
                    self.error_info = '操作超时！该条数据可以重新使用'
                self.errorList.append(self.u_name)
        except Exception as e:
            print(e)
            self.error_info = '未知错误！该条数据可以重新使用'
            logger.error('未知错误！', exc_info=True)
            self.errorList.append(self.u_name)
        finally:
            print('流程完毕！')
            # time.sleep(10)
            self.driver.quit()
            # 验证码重试三次

    # 接收5美金流程
    def accept_five(self):
        # next_button
        receive_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.ppvx_btn.ppvx_btn--inverse'))
        )
        # 点击接受按钮
        receive_btn.click()
        time.sleep(3)
        # claimfunds_cip
        keep_in_pp_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[name=claimfunds_cip]'))
        )
        keep_in_pp_btn.click()
        time.sleep(3)
        # nextButton
        # 偶尔提示，同意并继续页面
        try:
            next_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'nextButton'))
            )
            if next_button:
                next_button.click()
        except TimeoutException:
            logger.info('不存在同意并提示弹框！')
        time.sleep(5)
        # 输入生日
        # 生日文本框 id#date_of_birth
        # 输入社会安全号
        # 安全号后四位 id#ssn
        # 确认按钮 button[name=submit]
        birth_input = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, 'date_of_birth'))
        )
        ssn_input = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, 'ssn'))
        )
        time.sleep(3)
        if '-' in self.u_birth_day:
            birth_arr = self.u_birth_day.split('-')
        elif '/' in self.u_birth_day:
            birth_arr = self.u_birth_day.split('/')
        else:
            birth_arr = []
        if len(birth_arr) == 3:
            int_month = int(birth_arr[1])
            if int_month < 10:
                birth_input.send_keys('0')
                birth_input.send_keys(birth_arr[1])
            else:
                birth_input.send_keys(birth_arr[1])
            int_day = int(birth_arr[2])
            if int_day < 10:
                birth_input.send_keys('0')
                birth_input.send_keys(birth_arr[2])
            else:
                birth_input.send_keys(birth_arr[2])
            birth_input.send_keys(birth_arr[0])
            # birth_input.send_keys(birth_arr[1])
            # birth_input.send_keys(birth_arr[2])
        else:
            self.errorList.append(self.u_name)
            logger.error('解析生日格式出错！')
        # 输入社会安全码
        time.sleep(3)
        last_four_code = self.u_safe_code[-4:]
        logger.info('社会安全码：')
        logger.info(last_four_code)
        ssn_input.send_keys(last_four_code)
        # 点击确认按钮
        ok_button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[name=submit]'))
        )
        ok_button.click()
        # 增加完成弹框验证
        has_done = False
        try:
            done_link = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a.ppvx_btn___5-7-4'))
            )
            if done_link:
                has_done = True
                done_link.click()
        except Exception as e:
            print(e)
            logger.error('识别完成弹框出错！', exc_info=True)
        # 如果弹出完成提示，页面会跳到首页，直接去转账
        if has_done:
            time.sleep(5)
            try:
                self.pay_to_account()
            except Exception as e:
                print(e)
                self.error_type = '5'
                self.error_info = '填写成功，打款失败'
                logger.error('打款未成功！', exc_info=True)
        else:
            # 判断是否出错
            # div#home_address.error
            # has_error = False
            # 判断ssn错误
            self.error_type = '4'
            self.error_info = '未填写成功，其他错误'
            try:
                ssn_error = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input#ssn.error'))
                )
                if ssn_error:
                    self.error_type = '4'
                    self.error_info = 'ssn出错'
                    self.errorList.append('ssn出错，该条数据需要人工处理！')
            except TimeoutException:
                logger.info('ssn正常！')
            try:
                address_error = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div#home_address.error'))
                )
                if address_error:
                    self.error_type = '4'
                    self.error_info = '地址栏出错误，该条数据需要人工处理！'
                    self.errorList.append('地址栏出错误，该条数据需要人工处理！')
            except TimeoutException:
                logger.info('地址栏正常！')
            # time.sleep(500)
            # 领取完成之后回到转账界面
            # if not has_error:
            #     self.pay_to_account()

    def ling_quan(self):
        self.driver.get(self.gift_url)
        time.sleep(3)
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
        if 'you should receive your $5' in info_hero_text:
            # 领券成功
            logger.info('领券成功！')
            self.error_type = '3'
            self.lq_success_list = self.account
            # 跳转到总览页面
            self.driver.get(self.summary_url)
            time.sleep(5)
            #  判断接受款项按钮是否存在
            # a.ppvx_btn.ppvx_btn--inverse
            self.accept_five()
        elif 'You may have claimed' in info_hero_text:
            self.errorList.append(self.u_name)
            self.error_type = '1'
            self.error_info = '领券失败！'
            logger.error('没有购物券，领券失败，退出流程！')

    # 付款到指定账号
    def pay_to_account(self):
        # 跳转到付款界面
        self.driver.get(self.transfer_url)
        accept_money_input = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, 'fn-sendRecipient'))
        )
        accept_money_input.send_keys(self.u_pay_account)
        # time.sleep(500)
        # 判断下一页按钮是否可用
        next_btn = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type=submit]'))
        )
        # next_btn.click()
        next_btn.send_keys(Keys.ENTER)
        time.sleep(5)
        # 输入金额 继续
        # input#fn-amount
        fk_input = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, 'fn-amount'))
        )
        fk_input.send_keys(500)
        time.sleep(3)
        # button.css-uobemr.vx_btn
        fk_jx_btn = WebDriverWait(self.driver, 15).until(
            # css-1mggxor vx_btn
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.css-1mggxor.vx_btn'))
            # EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.vx_btn'))
        )
        fk_jx_btn.click()
        # fk_jx_btn.send_keys(Keys.ENTER)
        time.sleep(3)
        # 选择方式 继续
        # button.vx_btn.ctaButton
        # 三种弹框方式
        # 1
        try:
            qr_jx_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.vx_btn.ctaButton'))
            )
            qr_jx_btn.click()
        except Exception as e:
            print(e)
            logger.info('没有确认收货提示！')
        # 2
        try:
            qr_jx_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[name=goodsPayment]'))
            )
            qr_jx_btn.click()
        except Exception as e:
            print(e)
            logger.info('没有第二种提示！')

        # 3
        try:
            qr_jx_btn = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'label.purchaseLabel'))
            )
            qr_jx_btn.click()
            time.sleep(3)
            # self.driver.execute_script("arguments[0].click();", qr_jx_btn)
            jx_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.sendBtn'))
            )
            jx_btn.click()
        except Exception as e:
            print(e)
            logger.info('没有第三种提示！')
            # self.errorList.append(self.account)
            # self.ling_quan()
        # 立即发送付款
        # button.button.css-1mggxor.vx_btn
        # css-uobemr vx_btn
        time.sleep(3)
        lj_fs_btn = WebDriverWait(self.driver, 15).until(
            # css-uobemr vx_btn
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button.vx_btn'))
        )
        # lj_fs_btn.click()
        logger.info(lj_fs_btn)
        self.driver.execute_script("arguments[0].click();", lj_fs_btn)
        time.sleep(3)
        # h2.successHeader
        h2_text_el = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h2.successHeader'))
        )
        info_hero_text = h2_text_el.get_attribute('textContent')
        logger.info(info_hero_text)
        if '5.00 USD' in info_hero_text:
            logger.info('付款流程成功!')
            self.successList.append(True)
        else:
            if info_hero_text:
                logger.info('付款流程成功! 未判断文本!')
                self.successList.append(True)
        # 等待3秒
        time.sleep(3)


if __name__ == '__main__':
    # print('currentLine')
    # print(currentLine)
    # 登录链接
    sign_url = 'https://www.paypal.com/us/signin'
    # 领券链接
    gift_url = 'https://www.paypal.com/us/webapps/mpp/pfs/welcome/offer/mobile/5'

    # https://www.paypal.com/myaccount/transfer/homepage
    # fn-sendRecipient
    # button[type=submit]

    # 用户名、密码
    # u_name = '3437a7f@gmail.com'
    # u_pwd = '@As541287'
    # u_birth_day = '1978/7/31'
    # u_safe_code = '505237351'
    # u_pay_account = 'Patriciaedwardsibl8493@mail.ru'
    u_name = '7849604@gmail.com'
    u_pwd = '@As538709'
    u_birth_day = '1929/1/9'
    u_safe_code = '513241690'
    u_pay_account = 'vdegyh@163.com'

    # 3942d52@gmail.com-----@As572869-----1984-5-22----514943870----有---测试用
    # 0184f4a@gmail.com--------@As509827-----1983-12-27----514868086----有---测试地址错误
    # 3437a7f@gmail.com一@As541287一1978/7/31一505237351
    # dd92aa1@gmail.com一@As551734一1978/9/15一512942174

    logAndSignIns = LoginAndSign(u_name, u_pwd, u_birth_day, u_safe_code, u_pay_account, sign_url, gift_url)
    logAndSignIns.play()
