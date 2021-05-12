import re
import time

from selenium import webdriver
import requests
from PIL import Image
from pyquery import PyQuery as pq

# 网站url
mainUrl = "https://www.astost.com/bbs"
# 登录页面url
loginUrl = mainUrl + "/login.php"
# EX板块url
EXUrl = mainUrl + '/thread.php?fid=49'

# 遍历EX板块时获取页面的时间间隔
refreshInterval = 0.3

# chrome驱动要与本地安装的chrome的版本对应
# 下载地址:http://npm.taobao.org/mirrors/chromedriver/
executable_path = r"C:\Program Files\Google\Chrome\Application\chromedriver.exe"

# 登录信息
userName = 'n43635'
passWord = 'mzfndln43635'




options = webdriver.ChromeOptions()
# 忽略证书错误
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

browser = webdriver.Chrome(executable_path = executable_path,options = options)
# browser = webdriver.Chrome(executable_path=chrome_driver）

browser.get(loginUrl)                # 进入相关网站
html = browser.page_source          # 获取网站源码
# data = str(pq(html))            # str() 函数将对象转化为适于人阅读的形式。

# time.sleep(1)

# 点击验证码输入框以显示验证码
browser.find_element_by_name("gdcode").click()
loginCode = input('输入验证码: ')

# 填入相关数据
time.sleep(0.5)
browser.find_element_by_name("pwuser").clear()
browser.find_element_by_name("pwuser").send_keys(userName)

browser.find_element_by_name("pwpwd").clear()
browser.find_element_by_name("pwpwd").send_keys(passWord)

browser.find_element_by_name("gdcode").clear()
browser.find_element_by_name("gdcode").send_keys(loginCode)

browser.find_element_by_name("submit").click()

# 保存cookie
Cookies = browser.get_cookies()
# print(Cookies)

# 不加载图片，提升加载速度
prefs = {"profile.managed_default_content_settings.images":2}
options.add_experimental_option("prefs",prefs)

# 不加载图片需要启动一个新的浏览器
exbrowser = webdriver.Chrome(executable_path = executable_path,options=options)
exbrowser.get(loginUrl)
for cookie in Cookies:
    # print(cookie)
    exbrowser.add_cookie(cookie)

# 关闭登录浏览器
browser.quit()

# 获取EX板块数据
exbrowser.get(EXUrl)                # 进入相关网站
html = exbrowser.page_source          # 获取网站源码
time.sleep(0.3)

# 总页数获取
pageNum = re.findall(r'Pages:\s*\(\s*1/(.*?)\s*total\s*\)', html)[0]
print('一共有' + pageNum + '页')

# 遍历需要的数据并写入本地文件
with open("EX.html", 'a', encoding='utf-8') as f:
    f.write("<HTML><BODY>\n")

    # 倒数循环遍历页数
    for j in range(int(pageNum), 0, -1):

        # 进入最后一页
        nowNum = (EXUrl + '&page=' + str(j))
        exbrowser.get(nowNum)
        html = exbrowser.page_source
        # print(html)

        getPostUrl = re.findall(r'id="a_ajax_\d*"', html)

        # 遍历当前页帖子列表
        for i in getPostUrl:
            print(i)
            PostId = re.findall(r'id="a_ajax_(.*?)"', i)[0]
            PostName = re.findall(i + r'>(.*?)</a>', html)[0]
            PostUrl = "https://www.astost.com/bbs/read.php?tid=" + PostId
            # PostUrl = re.findall(r'<a\s*href="(.*?)"\s*' + i, html)[0]
            f.write('<a href="' + PostUrl + '">' + PostName + '</a></br>\n')
        print('第' + str(j) + '页抓取完成')
        time.sleep(refreshInterval)
    f.write("</BODY></HTML>")
    print('爬虫完成!')

# browser.quit()
