"""
This script scrapes market.bisnis.com/rekomendasi page and then analyzes
each article to see keywords like stock tickers. Hopefully later in dev
we can analyze the sentiment of the article itself also.
"""
from bs4 import BeautifulSoup
import sys
import requests
import re

headers = {"User-Agent":"Mozilla/5.0"}

def get_tickers(url):
    tickers = {}
    # 4 all caps letter words that are NOT stock tickers
    unused_words = ['IHSG', 'BUMN', 'NEWS', 'LIVE', 'EMAS', 'KURS', 'FREE', 'PPKM']
        
    try:
        page=requests.get(url, headers=headers) 
    except Exception as e:    
        error_type, error_obj, error_info = sys.exc_info()      
        print('ERROR FOR LINK:',url)                        
        print(error_type, 'Line:', error_info.tb_lineno)

    soup = BeautifulSoup(page.text, "html.parser")

    for divs in soup.find_all('div', class_='col-sm-10', itemprop='articleBody'):
        used_tickers = []
        for ps in divs.find_all('p'):
            text = ps.text.strip()
            for tcker in re.findall('\\b([A-Z]([A-Z])([A-Z])([A-Z]))\\b', text):
                for tck in tcker:
                    if len(tck) == 4 and tck not in unused_words and tck not in used_tickers:
                        if tck in tickers:
                            tickers[tck] += 1
                        else:
                            tickers[tck] = 1
                        
                        used_tickers.append(tck)

    
    return tickers
