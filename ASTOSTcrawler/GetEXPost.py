import re
import time

from selenium import webdriver
import requests
from PIL import Image
from pyquery import PyQuery as pq

# chrome驱动要与安装的chrome的版本对应
# 下载地址:http://npm.taobao.org/mirrors/chromedriver/
chrome_driver = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
options = webdriver.ChromeOptions()
# 忽略证书错误
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
browser = webdriver.Chrome(chrome_driver,chrome_options=options)
# browser = webdriver.Chrome(executable_path=chrome_driver）

# s = requests.session()
# headers = {
#    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/55.0.2883.103 '
#                  'Safari/537.36',
#    'Connection': 'keep-alive'}
mainUrl = "https://www.astost.com/bbs/login.php"
# browser = webdriver.Chrome()    # 打开浏览器
browser.get(mainUrl)                # 进入相关网站
html = browser.page_source          # 获取网站源码
# data = str(pq(html))            # str() 函数将对象转化为适于人阅读的形式。

time.sleep(1)

# 点击验证码输入框以显示验证码
browser.find_element_by_name("gdcode").click()
# html = browser.page_source
# imgurl = re.findall(r'<img\s*src="(.*?)"', html)[0]
# print(imgurl)

# imgurl = "https://www.astost.com/bbs/" + imgurl
# imgbuf = s.get(imgurl)
#
# with open('code.png', 'wb')as fp:
#     fp.write(imgbuf.content)
#
# img = Image.open('code.png')
# img.show()

# data = {}
# data['pwuser'] = 'n43635'
# data['pwpwd'] = 'whsbgz90052236sx'
# data['totp_onecode'] = input('输入验证码: ')

# 登录信息
userName = 'n43635'
passWord = 'mzfndln43635'
loginCode = input('输入验证码: ')

# 填入相关数据
time.sleep(0.5)
browser.find_element_by_name("pwuser").clear()
browser.find_element_by_name("pwuser").send_keys(userName)
time.sleep(0.1)
browser.find_element_by_name("pwpwd").clear()
browser.find_element_by_name("pwpwd").send_keys(passWord)
time.sleep(0.1)
browser.find_element_by_name("gdcode").clear()
browser.find_element_by_name("gdcode").send_keys(loginCode)
time.sleep(0.1)
browser.find_element_by_name("submit").click()
time.sleep(0.5)

# 获取EX板块数据
EXUrl = 'https://www.astost.com/bbs/thread.php?fid=49'
browser.get(EXUrl)                # 进入相关网站
html = browser.page_source          # 获取网站源码
time.sleep(1)

# 总页数获取
pageNum = re.findall(r'Pages:\s*\(\s*1/(.*?)\s*total\s*\)', html)[0]
print('一共有' + pageNum + '页')
time.sleep(1)

# 遍历需要的数据并写入本地文件
with open("EX.html", 'a', encoding='utf-8') as f:
    f.write("<HTML><BODY>\n")

    # 倒数循环遍历页数
    for j in range(int(pageNum), 0, -1):

        # 进入最后一页
        nowNum = (EXUrl + '&page=' + str(j))
        browser.get(nowNum)
        html = browser.page_source
        # print(html)

        getPostUrl = re.findall(r'id="a_ajax_\d*"', html)

        # 倒数循环遍历当前页帖子列表
        for i in reversed(getPostUrl):
            PostName = re.findall(i + r'>(.*?)</a>', html)[0]
            PostUrl = re.findall(r'<a\s*href="(.*?)"\s*' + i, html)[0]
            # print(PostName+PostUrl)
            # PostInfo = re.findall(r'<a href.*?'+ i + r'>.*?</a>', html)[0]
            f.write('<a href="https://www.astost.com/bbs/' + PostUrl + '">' + PostName + '</a></br>\n')
        print('第' + str(j) + '页抓取完成')
        time.sleep(0.5)
    f.write("</BODY></HTML>")
    print('爬虫完成!')

# browser.quit()
