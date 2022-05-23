from unittest import skipUnless
from bs4 import BeautifulSoup
import requests
from time import sleep 
def skipError(k):
    k = 0 

def parse(city , places):
    MainURL = 'https://www.delivery-club.ru'
    numPage = '/page{}'
    k = 0 
    domen = 'https://www.delivery-club.ru/'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 YaBrowser/22.1.5.810 Yowser/2.5 Safari/537.36'
    }
    for page in range(1,5):
        i = 0
        URL = MainURL + city
        if (page > 1):
            URL = MainURL + city + numPage.format(page)
        print(URL)
        response = requests.get(URL, headers=HEADERS)
        if response.status_code == 404:
            break
        
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.findAll('li', class_='vendor-item')

        for item in items:
            try:
                if (item.find('span', class_ ='rating__value rating__value--xsmall rating__value--yellow rating__value--medium rating--in-card__value').get_text(strip = True)):
                    places.append({
                        'title': item.find('h3', class_ ='vendor-item__title-text').get_text(strip = True),
                        'time': item.find('span', class_ ='vendor-item__delivery-time').get_text(strip = True),
                        'rate': item.find('span', class_='rating__value rating__value--xsmall rating__value--yellow rating__value--medium rating--in-card__value').get_text(strip=True).replace(",","."),
                        'link': ( domen + item.find('a',class_='vendor-item__link').get('href') )
                    })
            except AttributeError:
                skipError(k)
            
            try:
                if (item.find('span', class_ ='rating__value rating__value--xsmall rating__value--yellow rating__value--medium rating--in-card__value rating--in-card__value--high').get_text(strip = True)):
                    places.append({
                        'title': item.find('h3', class_ ='vendor-item__title-text').get_text(strip = True),
                        'time': item.find('span', class_ ='vendor-item__delivery-time').get_text(strip = True),  
                        'rate': item.find('span', class_='rating__value rating__value--xsmall rating__value--yellow rating__value--medium rating--in-card__value rating--in-card__value--high').get_text(strip=True).replace(",","."),
                        'link': ( domen + item.find('a',class_='vendor-item__link').get('href') )
                    })
            except AttributeError:
                skipError(k)
            try:
                if (item.find('span', class_ = 'rating__label rating__label--yellow rating__label--medium rating--in-card__label').get_text(strip = True)):
                    places.append({
                        'title': item.find('h3', class_ ='vendor-item__title-text').get_text(strip = True),
                        'time': item.find('span', class_ ='vendor-item__delivery-time').get_text(strip = True),
                        'rate': item.find('span', class_='rating__label rating__label--yellow rating__label--medium rating--in-card__label').get_text(strip=True).replace(",","."),
                        'link': ( domen + item.find('a',class_='vendor-item__link').get('href') )           
                    })            
            except AttributeError:
                skipError(k)
            i = i + 1
            
            if i == 23:
                    break
        sleep(2)
