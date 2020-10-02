import json

import requests

# 浏览器ua设置，网站需要哪些信息不确定，content-type是必须的
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63",
    "Host": "api.qingsuyun.com",
    "Origin": "https://www.qingsuyun.com",
    'Content-Type': 'application/json',
}


def Login():
    # 登录api地址
    logonApi = "https://api.qingsuyun.com/h5/api/login/login"
    factoryCode = 128968
    # 账户密码：json格式
    data = {"userCode": "496949238@qq.com", "password": "qBkxXcDT", "factoryCode": factoryCode}
    # 发送post请求，登录并获取cookies
    r_login = requests.post(url=logonApi, data=json.dumps(data), headers=headers, timeout=5)
    return r_login.cookies
