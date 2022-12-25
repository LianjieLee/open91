import subprocess

def download(url, name):
    cmd = ['/usr/local/bin/ffmpeg', '-hide_banner', '-i', f'{url}', '-c', 'copy', f'{name}']
    subprocess.run(cmd)

if __name__ == '__main__':
    download('https://cdn77.91p49.com//m3u8/589724/589724.m3u8', './output.mp4')
