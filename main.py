import os
import time
import pickle
from time import sleep
from selenium import webdriver

# 大麦网主页
bian_url = "https://www.binance.com/zh-CN"
# 登录页
login_url = "https://accounts.binance.com/zh-CN/login?return_to=aHR0cHM6Ly93d3cuYmluYW5jZS5jb20vemgtQ04vbmZ0L215c3RlcnktYm94"
# 抢票目标页
target_url = 'https://www.binance.com/zh-CN/nft/mystery-box'


class Concert:
    def __init__(self):
        option = webdriver.ChromeOptions()
        option.add_experimental_option(
            "excludeSwitches", ['enable-automation', 'enable-logging'])
        self.status = 0         # 状态,表示如今进行到何种程度
        self.login_method = 1   # {0:模拟登录,1:Cookie登录}自行选择登录方式
        self.driver = webdriver.Chrome(
            chrome_options=option)        # 默认Chrome浏览器

    def set_cookie(self):
        self.driver.get(bian_url)
        print("###请点击登录###")
        while self.driver.title.find('登录 | Binance') != -1:
            sleep(1)
        print('###请扫码登录###')

        while self.driver.title != '交易比特币、以太币和altcoin | 加密货币交易平台 | 币安':
            sleep(1)
        print("###扫码成功###")
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))
        print("###Cookie保存成功###")
        self.driver.get(target_url)

    def get_cookie(self):
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))  # 载入cookie
            for cookie in cookies:
                cookie_dict = {
                    'domain': '.binance.com',  # 必须有，不然就是假登录
                    'name': cookie.get('name'),
                    'value': cookie.get('value')
                }
                self.driver.add_cookie(cookie_dict)
            print('###载入Cookie###')
        except Exception as e:
            print(e)

    def login(self):
        if self.login_method == 0:
            self.driver.get(login_url)
            # 载入登录界面
            print('###开始登录###')

        elif self.login_method == 1:
            if not os.path.exists('cookies.pkl'):
                # 如果不存在cookie.pkl,就获取一下
                self.set_cookie()
            else:
                self.driver.get(target_url)
                self.get_cookie()

    def enter_concert(self):
        """打开浏览器"""
        print('###打开浏览器，进入币安###')
        self.driver.maximize_window()           # 最大化窗口
        # 调用登陆
        # self.login()                            # 先登录再说
        # self.driver.refresh()                   # 刷新页面
        self.status = 2                         # 登录成功标识
        print("###登录成功###")
        # 后续抢票流程


if __name__ == '__main__':
    try:
        con = Concert()             # 具体如果填写请查看类中的初始化函数
        con.enter_concert()         # 打开浏览器
        # con.choose_ticket()         # 开始抢

    except Exception as e:
        print(e)
        # con.finish()
