import time
import wx
import logging
from log import logger
import threading
import random
import string
import os
# import sys
import configparser
from register.auto_proxy import AutoChangeProxy

pass_str = string.ascii_letters
passNum = string.digits
passSymbol = '@#$&#!_'
emailStr = string.ascii_letters + string.digits + '_'
emailHz = ['hotmail.com', 'mail.com', 'yahoo.com', 'gmail.com']
base_r_path = r'C:\temp\register'
base_path = 'c:\\temp\\register\\'
conf_p = os.path.join(base_r_path, 'config.ini')
config = configparser.ConfigParser()


# 生成密码
def genPassword():
    key = random.sample(pass_str, random.randint(5, 10))
    key.extend(random.sample(passNum, random.randint(2, 6)))
    key.extend(random.sample(passSymbol, random.randint(1, 4)))
    # key[random.randint(1,len(key)-1)] = "$"
    # print(key)
    random.shuffle(key)
    keys = "".join(key)
    return keys


# 生成邮箱
def genEmail():
    key = random.sample(emailStr, random.randint(6, 12))
    keys = "".join(key)
    return keys + '@' + emailHz[random.randint(0, 3)]


# 判断数字类型
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass


# 日志控制
class WxTextCtrlHandler(logging.Handler):
    def __init__(self, ctrl):
        logging.Handler.__init__(self)
        self.ctrl = ctrl

    def emit(self, record):
        s = self.format(record) + '\n'
        wx.CallAfter(self.ctrl.WriteText, s)


# 拖拽到文本框
class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, parent):
        wx.FileDropTarget.__init__(self)
        self.table = parent.table
        self.parent = parent

    def OnDropFiles(self, x, y, filenames):
        logger.info('接收到文件')
        file_name = filenames[0]
        print(self.table.list.GetItemCount())
        if self.table.list.GetItemCount() > 0:
            confirm_exit = wx.MessageDialog(None, '列表里面已经包含数据，是否覆盖现有数据？', '确认框', wx.YES_NO | wx.ICON_QUESTION)
            if confirm_exit.ShowModal() == wx.ID_YES:
                self.handle_files(file_name)
                logger.info('覆盖列表！')
            else:
                logger.info('取消覆盖！')
                pass
        else:
            self.handle_files(file_name)
        return True

    def handle_files(self, file_name):
        if file_name and file_name.endswith('.txt'):
            logger.info(file_name)
            table_list = []
            with open(file_name, 'r') as fon:
                for line in fon.readlines():
                    print(line)
                    line = line.strip().replace("--------", "----")
                    line = line.replace("-----", "----")
                    account_list = line.split('----')
                    account_list.append('')
                    account_list.append('')
                    # account_list.append(genPassword())
                    table_list.append(account_list)
                    # logUtil.logger.debug(account_list)
            list_len = len(table_list)
            if list_len > 0:
                # 清空表
                self.table.clear_all_items()
                for item in table_list:
                    self.table.add_item(item)
                wx.MessageBox(f'成功导入{len(table_list)}条数据！', '提示', wx.OK | wx.ICON_INFORMATION)
            # 重新导入重置数据
            self.parent.error_count = 0
            self.parent.success_count = 0
            self.parent.current_loop_index = 0
            self.parent.all_lq_success_list = []
        else:
            wx.MessageBox('文件导入失败，请重新输入！', '提示', wx.OK | wx.ICON_ERROR)
        # for file in filenames:
        #     self.window.WriteText(file + '\n')


class MyFrame(wx.Frame):
    country_map = {'美国': 'US', '英国': 'UK', "德国": 'DE', "法国": 'FR', "西班牙": 'ES'}
    change_vpn_err_max = 3

    all_success_list = []
    all_error_list = []

    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)

        # 增加暂停功能
        self.is_pause = False
        self.current_loop_index = 0
        self.success_count = 0
        self.error_count = 0
        # 领券成功列表
        self.all_lq_success_list = []

        pnl = wx.Panel(self)
        pnl.SetAutoLayout(True)

        # print('hwnd:')
        # print(pnl.GetHandle())
        # print('bundle dir:')
        # print(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'driver', 'chromedriver.exe'))

        # 打开配置文件
        conf_info = config.read(conf_p)
        self.conf_len = len(conf_info)
        print('conf_info---------------')
        print(self.conf_len)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        label1 = wx.StaticText(pnl, 0, label=u'浏览器目录：')
        self.browser_path_input = wx.TextCtrl(pnl, 0, value="", size=(150, -1))
        self.browser_path_input.SetInsertionPoint(0)
        if self.conf_len > 0:
            self.browser_path_input.SetValue(config['DEFAULT']['browserpath'])
        # 911地址
        label_vpn = wx.StaticText(pnl, 0, label=u'911目录：')
        self.vpn_path_input = wx.TextCtrl(pnl, 0, value="", size=(150, -1))
        self.vpn_path_input.SetInsertionPoint(0)
        if self.conf_len > 0:
            self.vpn_path_input.SetValue(config['DEFAULT']['vpnpath'])
        # self.vpn_path_input.SetValue(r'C:\Users\Administrator\Desktop\911')

        hbox1.Add(label1, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 10)
        hbox1.Add(self.browser_path_input)

        hbox1.Add(label_vpn, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 10)
        hbox1.Add(self.vpn_path_input)

        #  hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        # label2 = wx.StaticText(pnl, label='国家：')
        # list1 = ['美国', '英国', "德国", "法国", "西班牙"]
        # self.country_list_ctrl = wx.ComboBox(pnl, -1, value='美国', choices=list1, style=wx.CB_SORT)
        # if self.conf_len > 0:
        #     self.country_list_ctrl.SetValue(config['DEFAULT']['country'])
        # self.country_list_ctrl.Disable()
        label3 = wx.StaticText(pnl, 0, label=u'切换VPN：')
        self.vpn_ctrl = wx.TextCtrl(pnl, 0, value="20", size=(30, -1))
        if self.conf_len > 0:
            self.vpn_ctrl.SetValue(config['DEFAULT']['vpnnumber'])
        # c_vpn.WriteText('5')
        # self.vpn_ctrl.Disable()
        # hbox1.Add(label2, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 10)
        # hbox1.Add(self.country_list_ctrl)
        hbox1.Add(label3, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 10)
        hbox1.Add(self.vpn_ctrl)

        vbox = wx.BoxSizer(wx.VERTICAL)

        # 按钮
        # hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.vpn_change_btn = wx.Button(pnl, label="切换vpn")
        hbox1.Add(self.vpn_change_btn, 0, wx.LEFT, 10)

        self.clear_all_btn = wx.Button(pnl, label="清空列表")
        hbox1.Add(self.clear_all_btn, 0, wx.LEFT, 10)

        self.start_btn = wx.Button(pnl, label="开始")
        hbox1.Add(self.start_btn, 0, wx.LEFT, 10)

        self.pause_btn = wx.Button(pnl, label="暂停")
        hbox1.Add(self.pause_btn, 0, wx.LEFT, 10)
        self.pause_btn.Disable()

        vbox.Add(hbox1, 0, flag=wx.ALL | wx.EXPAND, border=15)
        #  vbox.Add(hbox2,0,flag=wx.ALL | wx.EXPAND, border=5)
        #  vbox.Add(hbox3,0, wx.EXPAND | wx.ALL, 5)
        # 增删改
        operator_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # btn1 = wx.Button(pnl, label="增加")
        # btn2 = wx.Button(pnl, label="修改")
        # btn3 = wx.Button(pnl, label="导出")
        self.process_result = wx.StaticText(pnl, 0, label=u'执行结果：成功：0条，失败：0条')

        self.output_btn = wx.Button(pnl, label="打开输出结果目录")
        # self.output_btn.Disable()

        operator_sizer.Add(self.process_result, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 10)
        operator_sizer.Add(self.output_btn, 0, wx.LEFT | wx.ALL, 10)
        # operator_sizer.Add(btn2, 0, wx.ALL, 10)
        # operator_sizer.Add(btn3, 0, wx.ALL, 10)

        # self.Bind(wx.EVT_BUTTON, self.add_list, id=btn1.GetId())
        # self.Bind(wx.EVT_BUTTON, self.update_list, id=btn2.GetId())
        # self.Bind(wx.EVT_BUTTON, self.del_list, id=btn3.GetId())
        # 绑定开始方法
        self.Bind(wx.EVT_BUTTON, self.loop_table, id=self.start_btn.GetId())
        self.Bind(wx.EVT_BUTTON, self.pause_loop, id=self.pause_btn.GetId())
        self.Bind(wx.EVT_BUTTON, self.get_vpn_res, id=self.vpn_change_btn.GetId())
        self.Bind(wx.EVT_BUTTON, self.open_result_file, id=self.output_btn.GetId())
        self.Bind(wx.EVT_BUTTON, self.clear_table, id=self.clear_all_btn.GetId())
        # self.start_btn.Enable()
        vbox.Add(operator_sizer)
        # 列表
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.columns = [u'邮箱', u'密码', u'出生日期', u'社会安全码', u'收款账号', u'执行结果', u'描述']
        self.dataList = []
        self.table = Table(pnl, self.columns, self.dataList)

        sizer.Add(self.table.list, 1, wx.EXPAND, 10)
        vbox.Add(sizer, 1, wx.EXPAND | wx.ALL, 0)
        # 拖拽上传文件
        dt = MyFileDropTarget(self)
        self.table.list.SetDropTarget(dt)

        #  pnl1 = wx.Panel(self)

        #  pnl1.SetSizer(sizer)
        # 日志控制台
        log_sizer = wx.BoxSizer(wx.VERTICAL)
        log_label = wx.StaticText(pnl, 0, label=u'实时日志', style=wx.ALIGN_CENTRE_VERTICAL)
        log_label.SetSize(100, 50)
        log = wx.TextCtrl(pnl, wx.ID_ANY, size=(-1, 150), style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        log_sizer.Add(log_label, 0, wx.ALL, 5)
        log_sizer.Add(log, 1, wx.EXPAND, 10)
        handler = WxTextCtrlHandler(log)
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        logger.addHandler(handler)
        vbox.Add(log_sizer, 0, wx.EXPAND | wx.ALL, 0)

        pnl.SetSizer(vbox)
        self.Centre()

    def pause_loop(self, event):
        print('pause info')
        self.is_pause = True
        self.pause_btn.Disable()

    def clear_table(self, event):
        confirm_exit = wx.MessageDialog(None, '确认要清空表格数据吗？', '确认框', wx.YES_NO | wx.ICON_QUESTION)
        if confirm_exit.ShowModal() == wx.ID_YES:
            self.table.clear_all_items()
            self.current_loop_index = 0
            self.success_count = 0
            self.error_count = 0
            self.all_lq_success_list = []
            logger.info('列表已清空！')
        else:
            logger.info('取消清空！')
            pass

    # 打开执行结果目录
    def open_result_file(self, event):
        if self.table.list.GetItemCount() > 0:
            file_name = time.strftime("%Y-%m-%d_%H时", time.localtime()) + '_成功结果.txt'
            file_error_name = time.strftime("%Y-%m-%d_%H时", time.localtime()) + '_失败结果.txt'
            file_time_out_name = time.strftime("%Y-%m-%d_%H时", time.localtime()) + '_超时结果.txt'
            file_lq_success_name = time.strftime("%Y-%m-%d_%H时", time.localtime()) + '_领券成功未支付结果.txt'
            all_lq_success_name = time.strftime("%Y-%m-%d_%H时", time.localtime()) + '_所有领券成功结果.txt'
            success_list = []
            error_list = []
            time_out_list = []
            lq_success_list = []
            for idx in range(0, self.table.list.GetItemCount()):
                str_item = ''
                flag = 0
                split_str = '----'
                for col_index in range(0, 7):
                    text = self.table.list.GetItemText(idx, col_index)
                    if col_index < 5:
                        str_item = str_item + text + split_str
                    elif col_index == 5:
                        if text == '成功':
                            flag = 1
                        if text == '超时':
                            flag = 2
                        if text == '领券成功':
                            flag = 3
                        str_item = str_item + text + split_str
                    else:
                        str_item = str_item + text
                if flag == 1:
                    success_list.append(str_item + '\n')
                elif flag == 2:
                    time_out_list.append(str_item + '\n')
                elif flag == 3:
                    lq_success_list.append(str_item + '\n')
                else:
                    error_list.append(str_item + '\n')
            # 执行成功列表
            with open(base_path + file_name, 'w') as ff:
                for item in success_list:
                    ff.writelines(item)
            # 执行失败列表
            with open(base_path + file_error_name, 'w') as ff:
                for item in error_list:
                    ff.writelines(item)
            # 执行超时列表
            with open(base_path + file_time_out_name, 'w') as ff:
                for item in time_out_list:
                    ff.writelines(item)
            # 领券成功列表，支付未成功
            with open(base_path + file_lq_success_name, 'w') as ff:
                for item in lq_success_list:
                    ff.writelines(item)
            # 所有领券成功的数据
            if len(self.all_lq_success_list) > 0:
                # str_item = ''
                # split_str = '----'
                with open(base_path + all_lq_success_name, 'w') as ff:
                    for arr in self.all_lq_success_list:
                        try:
                            str_info = '----'.join(arr)
                            ff.writelines(str_info)
                        except Exception as e:
                            print(e)

        start_directory = base_r_path
        os.startfile(start_directory)

    # 切换vpn
    def get_vpn_res(self, event):
        # 判断911地址是否为空
        vpn_path_input_text = self.vpn_path_input.GetValue()
        # print(vpn_path_input_text)
        if vpn_path_input_text.strip() == '':
            wx.MessageBox('911代理地址不能为空！', '错误提示', wx.OK | wx.ICON_ERROR)
            return
        logger.info("vpn_path_input_text:" + vpn_path_input_text)
        hwnd = self.GetHandle()
        logger.info('hwnd:')
        logger.info(hwnd)
        change_proxy_ins = AutoChangeProxy(vpn_path_input_text)
        # country = self.country_map[self.country_list_ctrl.GetValue()]
        country = 'US'
        logger.info('国家：' + country)
        res = change_proxy_ins.change_ip('US', hwnd=str(hwnd))
        return res

    def chang_ctrl_status(self, disabled: bool):
        if not disabled:
            self.start_btn.Disable()
            # self.country_list_ctrl.Disable()
            self.vpn_ctrl.Disable()
            self.browser_path_input.Disable()
            # self.vpn_path_input.Disable()
            self.vpn_change_btn.Disable()
            self.clear_all_btn.Disable()
            self.pause_btn.Enable()
        else:
            self.browser_path_input.Enable()
            self.start_btn.Enable()
            # self.country_list_ctrl.Enable()
            self.vpn_ctrl.Enable()
            # self.vpn_path_input.Enable()
            self.vpn_change_btn.Enable()
            self.clear_all_btn.Enable()
            self.pause_btn.Disable()

    def add_list(self, event):
        print('add_list')
        self.table.add_item([4, 5, 6])
        logger.error('add error!')

    def update_list(self, event):
        pass

    def del_list(self, event):
        self.dataList.append([4, 5, 6])
        self.table.list.Refresh()

    def loop_table(self, event):

        # 判断浏览器地址是否为空
        browser_path_text = self.browser_path_input.GetValue()
        print(browser_path_text)
        if browser_path_text.strip() == '':
            wx.MessageBox('浏览器地址不能为空！', '错误提示', wx.OK | wx.ICON_ERROR)
            return

        # 判断vpn地址是否为空
        vpn_path_text = self.vpn_path_input.GetValue()
        print(vpn_path_text)
        if vpn_path_text.strip() == '':
            wx.MessageBox('911地址不能为空！', '错误提示', wx.OK | wx.ICON_ERROR)
            return

        # 判断切换代理切换间隔
        change_num = self.vpn_ctrl.GetValue()
        print(change_num)
        if self.vpn_ctrl.IsEmpty():
            wx.MessageBox('切换次数不能为空！', '错误提示', wx.OK | wx.ICON_ERROR)
            return

        if not is_number(self.vpn_ctrl.GetValue()):
            wx.MessageBox('切换次数必须是数字！', '错误提示', wx.OK | wx.ICON_ERROR)
            return
        # 切换次数
        vpn_number = int(self.vpn_ctrl.GetValue())
        # country_text = self.country_list_ctrl.GetValue()
        country_text = '美国'
        country = self.country_map[country_text]
        print(country)
        # 写入配置文件
        config['DEFAULT'] = {'BrowserPath': browser_path_text, 'VpnPath': vpn_path_text, 'VpnNumber': 10,
                             'Country': country_text}
        with open(conf_p, 'w') as configfile:
            config.write(configfile)

        if self.table.list.GetItemCount() == 0:
            wx.MessageBox('数据不能为空，请拖入数据到列表！', '错误提示', wx.OK | wx.ICON_ERROR)
            return
        # 停止暂停
        self.is_pause = False
        # 禁用开始按钮
        self.chang_ctrl_status(False)
        # 循环获取表格行信息
        son_thread = LoopTableThread(self, country, vpn_number)
        son_thread.start()


# class RegisterPaypalThread(threading.Thread):
#     def __init__(self, parent):
#         super(RegisterPaypalThread, self).__init__()
#         self.parent = parent
#         self.setDaemon(True)
#
#     def run(self):
class LoopTableThread(threading.Thread):
    def __init__(self, parent, country, vpn_number):
        super(LoopTableThread, self).__init__()
        self.parent = parent
        self.setDaemon(True)
        self.country = country
        self.vpn_number = vpn_number

    def run(self):
        current_index = 0
        print('开始执行任务：')
        # 根据国家切换对应国家的方法
        web_url = 'wx'
        from register.login_and_sign import LoginAndSign
        register_call = LoginAndSign

        logger.info(register_call)
        current_vpn_index = 0
        success_count = self.parent.success_count
        error_count = self.parent.error_count
        time_out_count = 0
        if web_url and register_call:
            ip = None
            for idx in range(self.parent.current_loop_index, self.parent.table.list.GetItemCount()):
                # 增加暂停功能
                if self.parent.is_pause:
                    self.parent.current_loop_index = idx
                    self.parent.success_count = success_count
                    self.parent.error_count = error_count
                    break

                col_count = self.parent.table.list.GetColumnCount() - 2
                col_count_last = self.parent.table.list.GetColumnCount() - 1
                # print(self.table.list.GetItem(col_count-1).GetText())
                # 切换vpn
                # if current_vpn_index == 0:
                #     self.parent.get_vpn_res(None)
                # else:
                #     current_vpn_index = current_vpn_index + 1
                # if current_vpn_index >= self.vpn_number or current_vpn_index == 0:
                #     current_vpn_index = current_vpn_index + 1
                #     if current_vpn_index > self.vpn_number:
                #         current_vpn_index = 1
                #     ip = self.parent.get_vpn_res(None)
                #     # 重试三次
                #     if not ip:
                #         ip = self.parent.get_vpn_res(None)
                #     if not ip:
                #         ip = self.parent.get_vpn_res(None)
                #     if not ip:
                #         ip = self.parent.get_vpn_res(None)
                # else:
                #     current_vpn_index = current_vpn_index + 1
                # logger.info('ip 地址：')
                # logger.info(ip)
                # if ip:
                #     wx.CallAfter(self.parent.table.list.SetItem, idx, col_count - 1, ip)
                # else:
                #     wx.CallAfter(self.parent.table.list.SetItem, idx, col_count - 1, '-')

                current_item = self.parent.table.list.GetItemText(idx)
                logger.info("current_item:")
                logger.info(current_item)
                # time.sleep(5)
                # test_num = random.randint(1, 10)
                # if test_num > 5:
                #     wx.CallAfter(self.parent.table.list.SetItem, idx, col_count, '成功')
                # else:
                #     wx.CallAfter(self.parent.table.list.SetItem, idx, col_count, '失败')

                # success_count = success_count + 1
                # wx.CallAfter(self.parent.process_result.SetLabelText,
                #              u'执行结果：成功：%d 条，失败：%d 条' % (success_count, error_count))
                # 实例化注册类

                account_list = []
                for col_index in range(0, 7):
                    text = self.parent.table.list.GetItemText(idx, col_index)
                    account_list.append(text)
                logger.info(account_list)
                # 登录链接
                sign_url = 'https://www.paypal.com/us/signin'
                # 领券链接
                gift_url = 'https://www.paypal.com/us/webapps/mpp/pfs/welcome/offer/mobile/5'
                # logger.info(current_item)
                register_ins = register_call(account_list[0], account_list[1], account_list[2], account_list[3],
                                             account_list[4], sign_url, gift_url)
                register_ins.play()
                success_list = register_ins.successList
                # 记录输出详情
                logger.info(register_ins.successList)
                logger.info(register_ins.errorList)
                # 赋值给领券成功列表
                if len(register_ins.lq_success_list) > 0:
                    self.parent.all_lq_success_list.append(register_ins.lq_success_list)

                is_time_out = False
                if len(success_list) > 0:
                    self.parent.all_success_list.append(success_list[0])
                    success_count = success_count + 1
                    wx.CallAfter(self.parent.process_result.SetLabelText,
                                 u'执行结果：成功：%d 条，失败：%d 条' % (success_count, error_count))
                    wx.CallAfter(self.parent.table.list.SetItem, idx, col_count, '成功')
                else:
                    self.parent.all_error_list.append(register_ins.account)
                    error_count = error_count + 1
                    wx.CallAfter(self.parent.process_result.SetLabelText,
                                 u'执行结果：成功：%d 条，失败：%d 条' % (success_count, error_count))
                    if register_ins.error_type == '3':
                        wx.CallAfter(self.parent.table.list.SetItem, idx, col_count, '领券成功')
                    elif register_ins.error_type == '2':
                        wx.CallAfter(self.parent.table.list.SetItem, idx, col_count, '超时')
                        time_out_count = time_out_count + 1
                        is_time_out = True
                    else:
                        wx.CallAfter(self.parent.table.list.SetItem, idx, col_count, '失败')

                    if register_ins.error_info:
                        wx.CallAfter(self.parent.table.list.SetItem, idx, col_count_last, register_ins.error_info)
                # 超时判断
                if is_time_out:
                    # 更换IP
                    self.parent.get_vpn_res(None)
                    time_out_count = 0
                    time.sleep(5)
                # 一次循环累计超时5次超时暂停循环
                if time_out_count == 5:
                    self.parent.pause_loop()

                # logger.info('idx:' + str(idx))
                # time.sleep(1)
            self.parent.chang_ctrl_status(True)
            self.parent.current_loop_index = 0
            # self.parent.output_btn.Disable()


# 表格增删改查
class Table(wx.ListCtrl):
    def __init__(self, parent, columns, data_list):
        super(Table, self).__init__()
        if columns is None:
            columns = []
        self.columns = columns
        self.dataList = data_list
        self.list = wx.ListCtrl(parent, -1, style=wx.LC_REPORT)
        # 设置表头
        for idx, colItem in enumerate(columns):
            self.list.InsertColumn(idx, colItem)
        # 设置数据
        for item in data_list:
            index_item = self.list.InsertItem(self.list.GetItemCount(), item[0])  # 插入项
            for idx, son in enumerate(item):
                self.list.SetItem(index_item, idx, str(son))

    def add_item(self, new_row: list):
        index_item = self.list.InsertItem(self.list.GetItemCount(), new_row[0])  # 插入项
        for idx, son in enumerate(new_row):
            self.list.SetItem(index_item, idx, str(son))

    # 清除表格数据
    def clear_all_items(self):
        self.list.DeleteAllItems()


def main():
    app = wx.App()
    frm = MyFrame(None, title='自动注册', size=(1000, 750))
    frm.Show()
    app.MainLoop()


if __name__ == '__main__':
    # pathname = 'C:\\temp\\register\\'
    # # if getattr(sys, 'frozen', False):
    # #     pathname = sys._MEIPASS
    # # else:
    # #     pathname = os.path.split(os.path.realpath(__file__))[0]
    # # global logUtil
    # pt = os.path.join(pathname, 'all.log')
    # print(pt)
    # # os.chmod(pt, 0o777)
    # # if not os.path.isfile(pt):
    # #     os.makedirs(pt)
    # with open(pt, mode='a', encoding='utf-8') as f:
    #     pass
    # logUtil = logger
    main()
#     # When this module is run (not imported) then create the app, the
#     # frame, show it, and start the event loop.
#     app = wx.App()
#     frm = MyFrame(None, title='注册', size=(900, 750))
#     frm.Show()
#     app.MainLoop()
