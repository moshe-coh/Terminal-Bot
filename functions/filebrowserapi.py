#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@Author  :   canwushuang 
@Version :   0.1
@Contact :   zhuangxiaohu@gmail.com
@Desc    :   Filebrowse API.
'''
import requests
import json

FbRoot = 'your filebrowser root path'
FbServer = 'http://127.0.0.1:18080'
headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5",
            "Content-Type": "application/json",
            "Host": FbServer,
            "Origin": FbServer,
            "Referer":f"{FbServer}/fb/login",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.34"
           }

def login(headers):
    url = f'{FbServer}/fb/api/login'
    #it can set in config.py also.this is demo.
    payload = {"username":"yourusername","password":"yourpassword","recaptcha":""}
    res = requests.post(url=url,headers=headers,data=json.dumps(payload))
    cookies = res.content
    headers['X-Auth'] = str(cookies,encoding = "utf-8")
    session = headers
    return session

def set_share(path, session):
    url = f'{FbServer}/fb/api/share{path}'
    print(url)
    payload = {"password":"","expires":"2","unit":"hours"}
    req = requests.post(url=url, headers = session, data=json.dumps(payload))
    res = json.loads(req.content)
    hash = res['hash']
    return hash

def run(path):
    root_folder = FbRoot
    if path.startswith(root_folder):
        cut = path.split(root_folder)
        session = login(headers)
        path = cut[-1]
        hash = set_share(path,session)
    else:
        pass
    return hash
        