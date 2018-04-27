# coding: utf-8

import urllib
import urllib2
import json
from lxml import etree
import requests

import urllib2
from bs4 import BeautifulSoup


class Splider:

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
                html_content = self.downloader.download(current_url)
                # new_url, data = self.parser.parse(root_url, html_content)
                # self.manager.add_new_url(new_url)
                # self.outputer.collect(data)
                self.outputer.output(html_content)
            except urllib2.URLError, e:
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
            # request = urllib2.Request(url, headers=headers)
            # response = urllib2.urlopen(request)
            response = requests.get(url, headers=header)
            content = response.text
        except urllib2.URLError, e:
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

    def parse(self, root_url, content):
        soup = BeautifulSoup(content, "html.parser", from_encoding="utf-8")
        div = soup.find(id="list-container")
        ul = div.find("ul", {"class": "note-list"})
        new_url = self.get_new_url(root_url, ul)
        new_data = self.get_new_data(root_url, ul)
        return new_url, new_data


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


if __name__ == "__main__":
    root_url = "https://api.gifskey.com/v1/gifs/trending?fmt=json&limit=20&lang=hindi&offset=40&rating="
    splider = Splider()
    splider.craw_search_word(root_url)
