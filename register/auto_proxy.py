import subprocess
import os
import random
from log import logger

'''
自动切换911 s5代理
'''
proxy_list = ['94', '93', '92', '90', '88', '86', '82', '81', '79', '77', '185', '176', '146', '95', '5', '37', '31',
              '213', '212', '159', '149', '87', '80', '46', '2', '194', '109', '62', '217', '151', '195', '51', '150',
              '84', '188', '193', '147', '134', '181', '89', '209', '143', '78']


class AutoChangeProxy:
    # exe = r'C:\Users\Administrator\Documents\911\ProxyTool\Autoproxytool.exe'
    # 911 代理路径
    exe = r'C:\Users\Administrator\Documents\911\ProxyTool\AutoProxyTool.exe'
    ip_list = list(range(1, 256))

    def __init__(self, vpn_path=None):
        logger.info('切换代理功能启动!')
        if vpn_path:
            self.exe = os.path.join(r'' + vpn_path, 'ProxyTool', 'AutoProxyTool.exe')

    def change_ip(self, country='GB', ip="23.*.*.*", hwnd=None):
        # param = r' -changeproxy/US/NY -proxyport=all -hwnd=test';
        # proc = None
        dir_path = os.getcwd()
        logger.info(dir_path)
        logger.info('切换代理开始...')
        result = None
        try:
            if hwnd:
                # ip = str(random.randint(1, 255)) + '.*.*.*'
                ip = random.choice(proxy_list) + '.*.*.*'
                logger.info('country:' + country + ',ip:' + ip + ',hwnd:' + hwnd)
                # logger.info(ip)
                self.proc = subprocess.run([self.exe, '-changeproxy/' + country],
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
