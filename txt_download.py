from bs4 import BeautifulSoup
import requests
import sys
"""
下载网络小说诛仙
"""


class downloader(object):

    def __init__(self):
        """
        定义类
        """
        self.server = 'http://www.biquge.com.tw/'
        self.target = 'http://www.biquge.com.tw/0_292/'
        self.names = []  # 存放章节名
        self.urls = []  # 存放章节链接
        self.nums = 0

    def get_download_url(self):
        """
        从目录页获取url列表
        """
        rep = requests.get(self.target)
        html = rep.content
        div_bf = BeautifulSoup(html)
        div = div_bf.find_all('div', id='list')
        a_bf = BeautifulSoup(str(div))
        a = a_bf.find_all('a')
        self.nums = len(a)
        for i in a:
            self.names.append(i.string)
            self.urls.append(self.server + i.get('href'))

    def get_contents(self, target):
        """
        从详情页获取内容
        """
        rep = requests.get(url=target)
        html = rep.content
        bf = BeautifulSoup(html)
        texts = bf.find_all('div', id='content')
        texts = texts[0].text.replace('\xa0'*4, '')
        return texts

    def writer(self, name, path, text):
        """
        将文章写入文档中
        """
        # write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)


if __name__ == "__main__":
    dl = downloader()
    dl.get_download_url()
    print('开始下载……')
    for i in range(dl.nums):
        dl.writer(dl.names[i], '诛仙.txt', dl.get_contents(dl.urls[i]))
        sys.stdout.write("已下载：%.1f%%" % float(100*i/dl.nums) + '\r')
        sys.stdout.flush()
    print('\n'+'下载完成')
