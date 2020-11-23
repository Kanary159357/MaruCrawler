from selenium import webdriver
import  requests
import shutil
def imgCrawler(URL):
    driver = webdriver.Chrome('Chrome/chromedriver.exe')
    driver.get(URL)

    elements = driver.find_elements_by_css_selector('div.view-img>img')
    cnt = 0
    print(len(elements))

    for element in elements:
        imgUrl = element.get_attribute('src')
        print(imgUrl)
        r = requests.get(imgUrl,stream = True)
        if r.status_code == 200:
            with open("img"+str(cnt)+".png", 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw,f)
        cnt+=1

if __name__ == "__main__":
    URL = 'https://marumaru.cash/bbs/cmoic/20033/145646'
    imgCrawler(URL)