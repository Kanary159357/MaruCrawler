from selenium import webdriver
import requests
import shutil
import os
import time
import copy
driver = webdriver.Chrome('Chrome/chromedriver.exe')


def createFolder(directory):
    os.makedirs(directory, exist_ok=True)


def ListCrawler(URL):
    driver.get(URL)
    comicName = driver.find_element_by_class_name('text-left').text
    comicList =driver.find_elements_by_class_name('list-subject>a')
    comicArray = []
    for item in comicList:
        comicArray.append([item.get_attribute('href'), item.text])
        print(comicArray[-1])

    print(len(comicList))
    createFolder('./' + comicName)
    for item in comicArray:
        comic_dir = './' + comicName + './' + item[1]
        createFolder(comic_dir)
        imgCrawler(item[0], comic_dir)



def imgCrawler(URL, directory):
    driver.get(URL)
    elements = driver.find_elements_by_css_selector('div.view-img>img')
    cnt = 0
    print(len(elements))

    for element in elements:
        imgUrl = element.get_attribute('src')
        print(imgUrl)
        r = requests.get(imgUrl, stream=True)
        if r.status_code == 200:
            with open(directory + '/' + str(cnt) + ".jpg", 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        cnt += 1


if __name__ == "__main__":
    URL = 'https://marumaru.cash/bbs/cmoic/19760'
    ListCrawler(URL)
