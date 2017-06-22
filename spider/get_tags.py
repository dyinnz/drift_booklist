"""
Simple script to get douban book tags.
You may need requests and beautifulsoup4 to use it.
Usage:
   python get_tags.py > tags.txt
"""
import requests
from bs4 import BeautifulSoup as bs

url = "https://book.douban.com/tag/"

r = requests.get(url)

soup = bs(r.text, 'lxml')

tables = soup.find_all('table', class_='tagCol')
for t in tables:
    for td in t.find_all('td'):
        print(td.a.string)
