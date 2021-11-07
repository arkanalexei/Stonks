"""
This program scrapes market.bisnis.com/rekomendasi page and then analyzes
each article to see keywords like stock tickers. Hopefully later in dev
we can analyze the sentiment of the article itself also.

** WARNING! **

Do NOT actually use this for stockpicking. Buying/selling stocks
from news recommendation alone is a TERRIBLE idea. Hence, DYOR!
"""
from bs4 import BeautifulSoup
import urllib.request,sys,time
import requests
import pandas as pd
from artikelscraping import get_tickers
from datetime import datetime

url = 'https://market.bisnis.com/rekomendasi'
headers = {"User-Agent":"Mozilla/5.0"}

judul = []
alamat = []

pages_to_get = 1

for i in range(1, pages_to_get + 1):
    print('page',i)
    url = url
    print('url',url)
    
    try:
        page=requests.get(url, headers=headers) 
    except Exception as e:    
        error_type, error_obj, error_info = sys.exc_info()      
        print('ERROR FOR LINK:',url)                        
        print(error_type, 'Line:', error_info.tb_lineno)

    time.sleep(2)
    soup = BeautifulSoup(page.text, "html.parser")
    
    for uls in soup.find_all('ul', class_='list-news'):

        for lis in uls.find_all('li'):
            for divs in lis.find_all('div', class_='col-sm-8'):
                for h2s in divs.find_all('h2'):
                    for ass in h2s.find_all('a'):
                        title = ass.get('title').strip()
                        link = ass.get('href')

                        judul.append(title)
                        alamat.append(link)


        for biglis in uls.find_all('li', class_='big style2'):
            for divs in biglis.find_all('div', class_='col-sm-6'):
                for h2s in divs.find_all('h2'):
                    for ass in h2s.find_all('a'):
                        title = ass.get('title').strip()
                        link = ass.get('href')

                        judul.append(title)
                        alamat.append(link)


    for nxt in soup.find_all('a', id='nextbtn'):
        nextpage = nxt.get('href')

    url = nextpage


data = pd.DataFrame(
    {
        'Judul':judul,
        'Alamat':alamat
    }
)

big_tickers = {}
countr = 1
for link_alamat in alamat:
#    time.sleep(2)
    print(f'artikel ke-{countr}:', link_alamat)
    the_tick = get_tickers(link_alamat)
    for key,value in the_tick.items():
        if key not in big_tickers:
            big_tickers[key] = 1
        else:
            big_tickers[key] += value
    
    countr += 1

data2 = pd.DataFrame(
    {
        'Ticker':big_tickers.keys(),
        'Jumlah':big_tickers.values()
    }
)


now = datetime.now()
# Saves excel file to current date and time
data2.sort_values('Jumlah', ascending=False).to_excel(f'{now.strftime("%Y%m%d, %H%M%S")}.xlsx')