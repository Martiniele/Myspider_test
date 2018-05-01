# coding: utf-8
import os
import json
import time

from lxml import etree
import requests


class Spider:

    def __init__(self):
        self.manager = Manager()
        self.downloader = Download()
        self.parser = Parse()
        self.outputer = Output()

    def craw_search_word(self, root_url):
        self.manager.add_new_url(root_url)
        while self.manager.has_new_url():
            try:
                current_url = self.manager.get_new_url()
                json_content = self.downloader.download(current_url)
                list = self.parser.parse(json_content)
                self.outputer.write_to_file(os.getcwd(), "gifs.txt", list, "a")
            except requests.ConnectionError as e:
                if hasattr(e, "reason"):
                    print "craw faild, reason: " + e.reason


class Manager(object):

    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    def add_new_url(self, new_url):
        if new_url is None:
            return None
        elif new_url not in self.new_urls and new_url not in self.old_urls:
            self.new_urls.add(new_url)

    def has_new_url(self):
        return len(self.new_urls) != 0

    def get_new_url(self):
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url


class Download(object):
    def download(self, url):
        if url is None:
            return None
        header = {
            "api_key": "4UEYojhUA694ZJ8SDlNT504p8AuUaZf524erKaIFuL83",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        content = ""
        try:
            response = requests.get(url, headers=header)
            content = response.text
        except requests.ConnectionError as e:
            if hasattr(e, "reason") and hasattr(e, "code"):
                print e.code
                print e.reason
            else:
                print "请求失败"
        return content


class Parse(object):

    def get_new_data(self, root_url, ul):
        data = set()
        lis = ul.find_all("li", {"class": "have-img"})
        for li in lis:
            cont = li.find("div", {"class": "content"})
            title = cont.find("a", {"class": "title"}).get_text()
            title_url = root_url + cont.a["href"]
            data.add((title, title_url))
        return data

    def get_new_url(self, root_url, ul):
        lis = ul.find_all("li", {"class": "have-img"})
        data_category_id = ul["data-category-id"]
        # 最后一个文章data-recommended-at －1
        max_id = int(lis[-1]["data-recommended-at"]) - 1
        new_url = root_url + "?data_category_id=" + data_category_id + "&max_id=" + str(max_id)
        return new_url

    def parse(self, content):
        list = []
        dict_1 = json.loads(content)
        list = dict_1["data"]
        return list


class Output(object):

    def __init__(self):
        self.datas = set()

    def collect(self, data):
        if data is None:
            return None
        for item in data:
            if item is None or item in self.datas:
                continue
            self.datas.add(item)

    def output(self, data):
        print data

    def write_to_file(self, path, file_name, content, mode='a'):
        if not os.path.isdir(path):
            os.makedirs(path)
        file_path = os.path.join(path, file_name)
        f = open(file_path, mode)
        idir = "gifsDir"
        ipath = str(path) + "\\" + str(idir)
        if not os.path.isdir(ipath):
            os.makedirs(ipath)


        for link in content:
            f.write(link["url"].encode("utf-8"))
            f.write("\n")
            self.dowload_gif_image(ipath, str(link["id"]) + ".gif", str(link["url"]))
        f.close()

    def dowload_gif_image(self, path, file_name, gifs_url):
        header = {
            "api_key": "4UEYojhUA694ZJ8SDlNT504p8AuUaZf524erKaIFuL83",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        path = path + "\\" + str(file_name)
        data = requests.get(gifs_url, headers=header)
        fil = file(path, "wb")
        fil.write(data.content)
        fil.close()


def main(max, limit, lang, type):
    spider = Spider()
    offset = 0
    while offset < max:
        root_url = "https://api.gifskey.com/v1/gifs/search?q={}&fmt=json&limit={}&lang={}&offset={}&rating=".format(str(type), int(limit),
                                                                                                                    str(lang), int(offset))
        spider.craw_search_word(root_url)
        offset += 20


if __name__ == "__main__":
    main(20, 20, "hindi", "crying")
