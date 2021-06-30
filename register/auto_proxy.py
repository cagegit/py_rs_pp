import subprocess
import os
import random
from log import logger

'''
自动切换911 s5代理
'''

proxy_list = ['89', '76', '172', '23', '98', '172', '162', '73', '76', '23', '174', '162', '97', '172', '73', '98',
              '24', '208', '73', '45', '47', '99', '73', '67', '66', '73', '185', '73', '47', '157', '73', '47', '157',
              '73', '45', '172', '47', '172', '69', '99', '77', '193', '45', '172', '108', '104', '172', '23', '38',
              '98', '76', '142', '108', '47', '66', '76', '104', '67', '174', '68', '76', '162', '216', '108', '76',
              '73', '198', '23', '172', '68', '47', '104', '98', '71', '75', '99', '157', '50', '73', '108', '107',
              '38', '24', '76', '68', '75', '185', '76', '91', '172', '135', '137', '174', '70', '107', '104', '107',
              '198', '170', '162', '166', '154', '204', '66', '73', '199', '172', '71', '68', '142', '24', '70', '206',
              '67', '191', '185', '157', '162', '103', '8', '198', '136', '154', '108', '174', '23', '99', '12', '216',
              '63', '69', '166', '104', '192', '174', '107', '68', '66', '173', '35', '162', '76', '193', '135', '142',
              '155', '97', '209', '130', '72']


class AutoChangeProxy:
    # exe = r'C:\Users\Administrator\Documents\911\ProxyTool\Autoproxytool.exe'
    # 911 代理路径
    exe = r'C:\Users\Administrator\Documents\911\ProxyTool\AutoProxyTool.exe'
    ip_list = list(range(1, 256))

    # param = r' -changeproxy/US/NY -proxyport=all -hwnd=test';
    # proc = subprocess.Popen([exe,'-changeproxy/','-ip=23.*.*.*'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    def __init__(self, vpn_path=None):
        logger.info('切换代理功能启动!')
        if vpn_path:
            self.exe = os.path.join(r'' + vpn_path, 'ProxyTool', 'AutoProxyTool.exe')

    def change_ip(self, country='US', ip="23.*.*.*", hwnd=None):
        # param = r' -changeproxy/US/NY -proxyport=all -hwnd=test';
        # proc = None
        dir_path = os.getcwd()
        logger.info(dir_path)
        # proc = subprocess.Popen([arg,'-changeproxy/US/NY','-freeport=all'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        logger.info('切换代理开始...')
        result = None
        try:
            if hwnd:
                # ip = str(random.randint(1, 255)) + '.*.*.*'
                ip = random.choice(proxy_list) + '.*.*.*'
                logger.info('country:' + country + ',ip:' + ip + ',hwnd:' + hwnd)
                # logger.info(ip)
                self.proc = subprocess.run([self.exe, '-changeproxy/' + country + '/CA'],
                                           stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                           shell=True)
                # self.proc = subprocess.getstatusoutput(r'' + self.exe + ' -changeproxy/' + country + ' -ip=' + ip +
                #                                        ' -hwnd=' + hwnd)
            else:
                self.proc = subprocess.Popen([self.exe, '-changeproxy/' + country, '-ip=' + ip], stdin=subprocess.PIPE,
                                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # out, err = self.proc.communicate(timeout=25)
            # proc.wait()
            # self.proc.wait()
            logger.info("911 vpn 返回结果：")
            logger.info(self.proc)
            logger.info('return code:')
            logger.info(self.proc.returncode)
            if self.proc.returncode != 0:
                logger.error('切换代理出错:')
                # print(err)
            else:
                # 等待3秒 等待程序ip切换完成
                # time.sleep(3)
                if self.proc.returncode == 0:
                    result = ip
                    logger.info('代理切换成功！')
        except Exception as e:
            # self.proc.kill()
            logger.error('执行切换代理命令出错', exc_info=True)
            print(e)
        # finally:
        # self.proc.kill()
        return result
