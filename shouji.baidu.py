#!/usr/bin/env Python
# coding=utf-8
import urllib.request
import urllib
import requests
from bs4 import BeautifulSoup
import socket
import random
import json
import os
import sys
import importlib

importlib.reload(sys)
threshold = 95  # favorable rate

retry = 0
# read a url and save the comments on the page to file
def get_page_code(url):# get the encode of the url
    request = urllib.request.Request(url)
    request.add_header('User-Agent',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36')
    try:
        response = urllib.request.urlopen(request, timeout=2)
        page_code = response.read()
        page_code = unicode(page_code,'GBK').encode('UTF_8')
        global retry
        retry = 0
        return page_code
    except urllib.request.URLError as e:
        print('网络错误:%s' % url)
        if retry < 5:
            retry += 1
            get_page_code(url)
    except UnicodeDecodeError as e:
        #print(e)
        try:
            return page_code.decode('gbk')
        except UnicodeDecodeError as ee:
            print(ee)
    except socket.timeout:
        print('超时:%s' % url)
        if retry < 5:
            retry += 1
            get_page_code(url)
    except Exception as e:
        print('其他错误 URL:' + url)
        print(e)
        if retry < 5:
            retry += 1
            get_page_code(url)


root = 'http://shouji.baidu.com/s?wd='
keyword = '赚钱'
after = '&data_type=app&f=header_all%40input&from=web_alad_multi'
url = root+keyword+after
res = get_page_code(url)
print (res)
