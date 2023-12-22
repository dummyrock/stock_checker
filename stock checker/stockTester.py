import time
import requests
import lxml
import re
from bs4 import BeautifulSoup
import buyingSelling

running = True

def buyCheck(stock):
    while running:

        ticker = re.sub('[\W\d_]+','',stock)
        
        newStock = getData(ticker)

        old = re.findall(r'\d+',stock)
        old = old[0] + '.' + old[1]
        old = float(old)

        new = re.findall(r'\d+',newStock)
        new = new[0] + '.' + new[1]
        new = float(new)

        if old < new:
            buyingSelling.selling(new)
            running = False
        time.sleep(180)

def getData(ticker):
    try:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0'}
            url = f'https://www.google.com/finance/quote/{ticker}:NASDAQ'
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, 'lxml')
            x = soup.find('div', {'class':'YMlKec fxKbKc'})
            stock = (f'{ticker} {x.text}')
            return stock
        except:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0'}
            url = f'https://www.google.com/finance/quote/{ticker}:NYSE'
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, 'lxml')
            x = soup.find('div', {'class':'YMlKec fxKbKc'})
            stock = (f'{ticker} {x.text}')
            return stock
    except:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0'}
        url = f'https://www.google.com/finance/quote/{ticker}:NYSEAMERICAN'
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        x = soup.find('div', {'class':'YMlKec fxKbKc'})
        stock = (f'{ticker} {x.text}')
        return stock
