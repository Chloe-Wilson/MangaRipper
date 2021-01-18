from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
import os

page = webdriver.Chrome()
page.get('http://mangareader.cc')
targets = []
while True:
    inputTarget = input('Manga Page : ')
    if inputTarget == '':
        break
    targets.append(inputTarget)
page.close()

for target in targets:
    try:
        dir = 'D:/Manga/' + target.split('/')[len(target.split('/')) - 1]
        try:
            os.mkdir(dir)
        except:
            pass

        response = requests.get(target)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True, title=True)
        links.pop(0)
        links = links[::-1]
        links.pop(0)

        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        driver = webdriver.Chrome(options=op)

        for link in links:
            try:
                os.mkdir(dir + '/' + link['title'])
            except:
                if os.path.isfile(dir + '/' + link['title'] + '/Done.txt'):
                    continue
            print(link['title'])
            driver.get(link['href'])
            try:
                select = Select(driver.find_elements_by_tag_name('select')[1])
            except:
                f = open('error.txt', 'a+')
                f.write(link['title'] + '\n')
                f.close()
                continue
            select.select_by_index(1)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            picture = 0
            for pic in soup.find_all('img'):
                if 'lazy' in str(pic):
                    picture += 1
                    response = requests.get(pic['src'])
                    file = open(dir + '/' + link['title'] + '/' + str(picture) + '.jpg', 'wb')
                    file.write(response.content)
                    file.close()
            file = open(dir + '/' + link['title'] + '/Done.txt', 'w+')
            file.close()
    except Exception as e:
        pass

