import os
import urllib.request, urllib.parse, urllib.error
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as soup
import time
import json
from collections import OrderedDict

# 인스타그램 로그인 URL
loginUrl = 'https://www.instagram.com/accounts/login/'

# driver load
driver = wd.Chrome(executable_path='./chromedriver')

driver.implicitly_wait(5)

# 웹 사이트 접속
driver.get(loginUrl)

# 사전 정보 정의
username = '계정명'
userpw = '비밀번호'
hashTag = 'applewatch4'
hashLink = '//a[@href="/explore/tags/'+hashTag+'/"]'

# 로그인 정보 입력
driver.find_element_by_name('username').send_keys(username)
driver.find_element_by_name('password').send_keys(userpw)

driver.implicitly_wait(5)
driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button').submit()

# 태그 입력
driver.find_element_by_xpath("""//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input""").send_keys(hashTag)
driver.implicitly_wait(8)

# 해시태그 URL
tagUrl = 'https://www.instagram.com/explore/tags/' + hashTag + '/'

# 옵션 추가 (브라우저 띄우지 않음)
options = wd.ChromeOptions()	
options.add_argument('headless')	
options.add_argument('disable-gpu')	
driver = wd.Chrome(executable_path='./chromedriver', options=options)

driver.implicitly_wait(5)

# 웹 사이트 접속
driver.get(tagUrl)

images = driver.find_elements_by_tag_name('img')
data = OrderedDict()

count = 0
for img in images:
  data[str(count)] = {'src':img.get_attribute('src')}
  count += 1
  if count == 100:
    break

with open('search.json', 'w', encoding='utf-8') as file:
  json.dump(data, file, ensure_ascii=False, indent='\t')

driver.quit()