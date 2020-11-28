from selenium import webdriver
import requests
import shutil
import os
import tkinter
import re
from urllib.parse import urlparse
from tkinter import filedialog


class MaruCrawler:
    URL = None
    def __init__(self, URL):
        self.URL = URL
        self.dir_path = "/"
        self.driver = webdriver.Chrome('Chrome/chromedriver.exe')
    def temp(self):
        self.driver.get(self.URL)
        name = self.driver.find_element_by_xpath("//meta[@name='title']").get_attribute('content')
        print(name)
        self.driver.quit()

    def initCrawler(self):
        regex = re.compile("/\d+")
        p_url = urlparse(self.URL)
        m = regex.findall(str(p_url.path))
        #print(self.URL)
        print(m)
        if len(m) == 1 :
            self.ListCrawler()
        else :
            self.imgCrawler(self.URL)

    def openFolder(self):
        root = tkinter.Tk()
        root.withdraw()
        dir_path = filedialog.askdirectory(parent=root, initialdir = "/", title='Please select the directory')
        print("\n dir_path : ", dir_path)

    def createFolder(self, directory):
        os.makedirs(directory, exist_ok=True)

    def ListCrawler(self):
        self.driver.get(self.URL)
        comicName = self.driver.find_element_by_css_selector('h1.text-left')
        comicList = self.driver.find_elements_by_class_name('list-subject>a')
        comicArray = []
        print(comicName)
        for item in comicList:
            comicArray.append([item.get_attribute('href'), item.text])
            print(comicArray[-1])

        print(len(comicList))
        list_dir = './' + comicName.text + '/'
        self.createFolder(list_dir)
        for item in comicArray:
            self.imgCrawler(item[0], list_dir)

    def imgCrawler(self, url, directory= "./"):
        self.driver.get(url)
        name = self.driver.find_element_by_xpath("//meta[@name='title']").get_attribute('content')
        comic_dir = directory + name
        self.createFolder(comic_dir)
        elements = self.driver.find_elements_by_css_selector('div.view-img>img')
        cnt = 0
        print(len(elements))

        for element in elements:
            imgUrl = element.get_attribute('src')
            print(imgUrl)
            r = requests.get(imgUrl, stream=True)
            if r.status_code == 200:
                with open(comic_dir + './' + str(cnt) + ".jpg", 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
            cnt += 1


if __name__ == "__main__":
    URL = 'https://marumaru.loan/bbs/cmoic/19659/20'
    #openFolder()
    #ListCrawler(URL)
    MaruCrawler(URL).initCrawler()
