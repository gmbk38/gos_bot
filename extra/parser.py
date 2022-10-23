import urllib
import urllib.parse
import urllib.request
import requests
from bs4 import BeautifulSoup

url = 'https://yandex.ru/pogoda/moscow?lat=55.755863&lon=37.6177'

page = BeautifulSoup(urllib.request.urlopen(url), 'lxml')
# print(page)

for el in page.find_all('div', class_='content content_compressed i-bem'):
