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
refreshInterval = 0.5

# chrome驱动要与本地安装的chrome的版本对应
# 下载地址:http://npm.taobao.org/mirrors/chromedriver/
executable_path = r"C:\Program Files\Google\Chrome\Application\chromedriver.exe"

# 登录账户信息
userName = 'n43635'
passWord = 'mzfndln43635'


options = webdriver.ChromeOptions()
# 忽略证书错误
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

browser = webdriver.Chrome(executable_path = executable_path,options = options)    # 先开启webdriver，主要为之后获取cookie信息
browser.get(loginUrl)                # 进入登录页面
html = browser.page_source          # 获取网站源码

# 点击验证码输入框以显示验证码
browser.find_element_by_name("gdcode").click()
loginCode = input('输入验证码: ')

# 填入登录信息执行登录操作
browser.find_element_by_name("pwuser").clear()
browser.find_element_by_name("pwuser").send_keys(userName)
browser.find_element_by_name("pwpwd").clear()
browser.find_element_by_name("pwpwd").send_keys(passWord)
browser.find_element_by_name("gdcode").clear()
browser.find_element_by_name("gdcode").send_keys(loginCode)
browser.find_element_by_name("submit").click()

Cookies = browser.get_cookies()    # 保存cookie
prefs = {"profile.managed_default_content_settings.images":2}    # 设置不加载图片，提升加载速度
options.add_experimental_option("prefs",prefs)
browser.quit() # 关闭登录浏览器
exbrowser = webdriver.Chrome(executable_path = executable_path,options=options)    # 不加载图片需要启动一个新的webdriver
exbrowser.get(loginUrl)

# 将cookie插入到新的webdriver中
for cookie in Cookies:
    exbrowser.add_cookie(cookie)

exbrowser.get(EXUrl)                # 进入EX板块页面
html = exbrowser.page_source          # 获取网站源码
time.sleep(0.3)

# 总页数获取
pageNum = re.findall(r'Pages:\s*\(\s*1/(.*?)\s*total\s*\)', html)[0]
print('一共有' + pageNum + '页')

nowTime = time.strftime("(%Y-%m-%d %H-%M-%S)", time.localtime()) 
fileName = "EX" + nowTime + ".html" 

# 遍历需要的数据并写入本地文件
with open(fileName, 'a', encoding='utf-8') as f:
    f.write("<HTML><BODY>\n")
    # 从第一页开始循环遍历
    for j in range(0, int(pageNum), 1):
        nowNum = (EXUrl + '&page=' + str(j))
        exbrowser.get(nowNum)
        html = exbrowser.page_source
        getPostUrl = re.findall(r'id="a_ajax_(.*?</)', html)    # 从页面获取帖子需要的数据
        postList = ''
        # 遍历数据
        for i in getPostUrl:
            PostId = re.findall(r'(\d+)"', i)[0]    # 截取Id
            PostName = re.findall(r'>([^<>]*)</', i)[0]    # 截取帖子主题名
            PostUrl = "https://www.astost.com/bbs/read.php?tid=" + PostId    # url是通过id拼接成的
            postList = postList + '<a href="' + PostUrl + '">' + PostName + '</a></br>\n'
        f.write(postList)    # 重组当前页面的数据结构，并一次性写入到文件中
        print('第' + str(j+1) + '页抓取完成')
        time.sleep(refreshInterval)
    f.write("</BODY></HTML>")
    print('爬虫完成!')

# browser.quit()
