"""
This script scrapes IMDB's top 250 movies of all time and returns
a random movie from it
"""
from bs4 import BeautifulSoup
import sys
import requests
import pandas as pd

url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
headers = {"User-Agent":"Mozilla/5.0"}
movies = []

GET_NEW_MOVIE_TITLES = False

if GET_NEW_MOVIE_TITLES:

    try:
        page=requests.get(url, headers=headers) 
    except Exception as e:    
        error_type, error_obj, error_info = sys.exc_info()      
        print('ERROR FOR LINK:',url)                        
        print(error_type, 'Line:', error_info.tb_lineno)

    soup = BeautifulSoup(page.text, "html.parser")

    for tds in soup.find_all('td', class_='titleColumn'):
        for ass in tds.find_all('a'):
            movies.append(ass.text)

    data = pd.DataFrame(
        {
            'judul':movies
        }
    )

    data.to_excel(f'movies.xlsx', index=False)

else:
    excel = pd.read_excel('movies.xlsx')

    print(excel.sample())

