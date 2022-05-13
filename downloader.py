import subprocess

def download(url, name):
    cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', url, '-c', 'copy', name]
    subprocess.run(cmd)

if __name__ == '__main__':
    download('https://cdn77.91p49.com//m3u8/589724/589724.m3u8', './output.mp4')
