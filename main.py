#!/usr/bin/python3
import os
import json
import time
import requests
from faker import Faker
from bs4 import BeautifulSoup
from urllib.parse import urlparse,parse_qs

from parser import parse
from downloader import download


class Porn:
    def __init__(self, name):
        self.name = name
        self.new_key = []
        with open(f'{name}.json') as f:
            self.old_key = json.load(f)

    # 获取视频链接列表
    def getVideoList(self, url):
        headers = {'User-Agent': Faker().user_agent(),
                   'X-Forwarded-For': Faker().ipv4(),
                   'Referer': 'http://www.91porn.com/index.php',
                   'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        playlist = soup.find_all('div', {'class': 'col-xs-12 col-sm-4 col-md-3 col-lg-3'}) #已失效，页面中href链接已被加密
        for i in playlist:
            link = i.find('a')['href']
            key = parse_qs(urlparse(link).query)["viewkey"][0]
            if key not in self.old_key:
                self.new_key.append(key)
        print(time.strftime('%Y-%m-%d %H:%M:%S'), f'待获取{self.name}视频{len(self.new_key)}个', flush=True)

    def updateList(self):
        self.old_key = self.old_key[-240:len(self.old_key)]
        with open(f'{self.name}.json', 'w') as f:
            json.dump(self.old_key, f)
        print(time.strftime('%Y-%m-%d %H:%M:%S'), f'{self.name}列表信息更新完毕', flush=True)

    def main(self, peer_name, page_list, start):
        for page in page_list:
            self.getVideoList(page)
        for key in self.new_key:
            if time.time()-start>5400:
                break
            # 解析视频直链
            try:
                link = f'http://www.91porn.com/view_video.php?viewkey={key}'
                title, poster, video, author = parse(link)
                print(time.strftime('%Y-%m-%d %H:%M:%S'), f'{title} 解析完毕！', flush=True)
            except Exception as e:
                print("提取视频直链过程：", e, flush=True)
                continue
            # 下载视频
            # print(f'video dl: {video}')
            try:
                name = os.getcwd() + f'/{key}.mp4'
                download(video, name)
                size = os.path.getsize(name)
                print(time.strftime('%Y-%m-%d %H:%M:%S'), f'{title} 下载完成！', flush=True)
            except Exception as e:
                print("下载视频过程：", e, flush=True)
                continue
            # 上传视频
            try:
                if size < 1024:
                    print(f'{title}  {size}byte < 1k, maybe get 403 page', flush=True)
                elif size < 100 * 1024:
                    print(f'{title} {size / 1024}k < 100k, may be get warning video', flush=True)
                else:
                    update = time.strftime('%Y%m%d')
                    msg = title + f"\nViewkey: {key}\n作者: #{author}\n日期: #on{update}"
                    os.system(f'python3 ./uploader.py {peer_name} {name} "{msg}" {poster}')
                    print(time.strftime('%Y-%m-%d %H:%M:%S'), f'{title} 上传完成！', flush=True)
                os.remove(name)
            except Exception as e:
                print("上传视频过程：", e, flush=True)
                continue
            self.old_key.append(key)
        self.updateList()


if __name__ == '__main__':
    start = time.time()
    all_video = Porn('all')
    hot_video = Porn('hot')
    all_peer_name = '@chan_91'
    hot_peer_name = '@hot_91'
    all_page = ['http://www.91porn.com/v.php',
                'http://www.91porn.com/v.php?page=2',
                'http://www.91porn.com/v.php?page=3',
                'http://www.91porn.com/v.php?page=4']
    hot_page = ['http://www.91porn.com/v.php?category=hot',
                'http://www.91porn.com/v.php?category=hot&page=2',
                'http://www.91porn.com/v.php?category=hot&page=3']
    all_video.main(all_peer_name, all_page, start)
    hot_video.main(hot_peer_name, hot_page, start)
