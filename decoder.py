import execjs
import requests
from faker import Faker
from bs4 import BeautifulSoup

# 需安装nodejs，npm，atob(npm)，jsdom(npm)
# https://github.com/zzjzz9266a/91porn_php/blob/master/detailPage.php
# url形式为http://91.9p9.xyz/ev.php?VID=
def decode(url, ip=None):
    prefix = """
                const atob = require('atob');
                const jsdom = require("jsdom");
                const { JSDOM } = jsdom;
                const dom = new JSDOM(`<!DOCTYPE html><p>Hello world</p>`);
                window = dom.window;
                document = window.document;
                XMLHttpRequest = window.XMLHttpRequest;
            """
    # http://91.9p9.xyz/js/m.js
    # http://www.91porn.com/js/m.js
    headers = {'User-Agent': Faker().user_agent()}
    js_res = requests.get('http://91.9p9.xyz/js/m.js', headers=headers)
    # print(js_res.apparent_encoding)
    # js_res.encoding = js_res.apparent_encoding
    js_res.encoding = 'gbk'
    js = prefix + js_res.text
    if ip:
        headers.update({'X-Forwarded-For': ip})
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    strcodes = soup.find('video', id="player_one").script.string.split('strencode(')[-1].split('))')[0].split(',')
    code0 = strcodes[0].replace('"', '')
    code1 = strcodes[1].replace('"', '')
    code2 = strcodes[2].replace('"', '')
    # C:\Users\Win10\AppData\Roaming\npm\node_modules
    myjs = execjs.compile(js, cwd=r"/usr/local/lib/node_modules")
    info = myjs.call('strencode', code0, code1, code2)
    return BeautifulSoup(info, 'html.parser').source['src']


def decode2(encstr):
    prefix = """
                const atob = require('atob');
                const jsdom = require("jsdom");
                const { JSDOM } = jsdom;
                const dom = new JSDOM(`<!DOCTYPE html><p>Hello world</p>`);
                window = dom.window;
                document = window.document;
                XMLHttpRequest = window.XMLHttpRequest;
            """
    headers = {'User-Agent': Faker().user_agent()}
    js_res = requests.get('http://www.91porn.com/js/m2.js', headers=headers)
    js_res.encoding = 'gbk'
    js = prefix + js_res.text    
    myjs = execjs.compile(js, cwd=r"/usr/local/lib/node_modules")
    info = myjs.call('strencode2', encstr)
    return BeautifulSoup(info, 'html.parser').source['src']

if __name__ == '__main__':
    encstr = "%3c%73%6f%75%72%63%65%20%73%72%63%3d%27%68%74%74%70%73%3a%2f%2f%63%64%6e%37%37%2e%39%31%70%34%39%2e%63%6f%6d%2f%6d%33%75%38%2f%36%31%39%32%36%32%2f%36%31%39%32%36%32%2e%6d%33%75%38%27%20%74%79%70%65%3d%27%61%70%70%6c%69%63%61%74%69%6f%6e%2f%78%2d%6d%70%65%67%55%52%4c%27%3e"
    print(decode2(encstr))
