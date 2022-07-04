import re
import requests
from bs4 import BeautifulSoup
from faker import Faker

from decoder import decode,decode2

def parse(url):
    headers = {'User-Agent': Faker().user_agent(),
               'X-Forwarded-For': Faker().ipv4(),
               'Referer': 'http://www.91porn.com/index.php',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.find('div', {'class': 'video-border'}).find('h4').text.strip()
    detail = soup.find_all('div', {'id': 'videodetails-content'})[1]
    author = detail.find_all('div')[1].find('span', {'class': 'title'}).text
    poster = soup.find('video', id="player_one")['poster']
    encvideo = re.search(r'strencode2\("(.*?)"\)', r.text)
    share_link = soup.find('textarea', {'id': "fm-video_link"})
    VUID = soup.find('div', id='VUID')
    if encvideo:
        video = decode2(encvideo.group(0))
    elif share_link:
        video = video = decode(share_link.text)
    else:
        video = decode(f'http://91.9p9.xyz/ev.php?VID={VUID.text}')
    return title, poster, video, author

if __name__ == '__main__':
    info = parse('http://www.91porn.com/view_video.php?viewkey=19db10a4128f16a963a7')
    print(info)
