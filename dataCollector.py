import requests
import lxml
import time
import csv
import re
import stockTester
import buyingSelling
from bs4 import BeautifulSoup
from multiprocessing import Pool

PERCENTAGE = 0.02

def getTicker():

    tickers = []
    
    CSV_URL = 'https://www.nasdaq.com/market-activity/stocks/screener'

    with open('nasdaq_screener_1677526712536.csv') as file:
        csvreader = csv.reader(file)

        next(csvreader)

        for row in csvreader:
            tickers.append(row[0])

    return tickers

def getData(ticker):
    try:
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
    except:
        return 'hp'
        print('error')
            
def analyzer(stockOldest,stockOld,stockNew):

    stocksToBuy = []
    stockListOld = []
    stockListNew = []

    for iteration, item in enumerate(stockOldest):
        oldest = re.findall(r'\d+',item)
        oldest = oldest[0] + '.' + oldest[1]
        oldest = float(oldest)
        old = re.findall(r'\d+',stockOld[iteration])
        old = old[0] + '.' + old[1]
        old = float(old)
        if old < oldest * 1 - PERCENTAGE:
            stockListOld.append(stockOld[iteration])

    print(stockListOld)
    

    for iteration, item in enumerate(stockListOld):
        old = re.sub('[\W\d_]+','',item)
        for stock in stockNew:
            st = re.sub('[\W\d_]+','',stock)
            if st == old:
                stockListNew.append(stock)

    
    for iteration, item in enumerate(stockListNew):
        new = re.findall(r'\d+',item)
        new = new[0] + '.' + new[1]
        new = float(new)
        old = re.findall(r'\d+',stockListOld[iteration])
        old = old[0] + '.' + old[1]
        old = float(old)
        if new > old * 1 + PERCENTAGE:
            stocksToBuy.append(item)
    print(f'buying: {stocksToBuy}')
    for item in stocksToBuy:

        stock = re.findall(r'\d+',item)
        stock = stock[0] + '.' + stock[1]
        stock = float(stock)

        buyingSelling.buying(stock)
        stockTester.buyCheck(item)
    
def main():

    listCount = 0
    
    while running:

        t = time.asctime()
        t = t.replace(':','_')
        f = open(f'E:\\storage\\files\\stock checker\\data\\{t}.txt', 'w')
        d = open('debugStockData.txt', 'w')
        tickerNames = []
        tickerData = []
        old = []
        oldest = []
        new = []

        if listCount == 3:      
            analyzedData = analyzer(oldest,old,new)


        tickerNamesData = getTicker()                            
        
        for ticker in tickerNamesData:
            ticker = ticker.rstrip('\n')
            index = ticker.count('^')
            if index == 0:
                    tickerNames.append(ticker)

        print(time.asctime())

        with Pool(30) as pool:
            for result in pool.map(getData,tickerNames):
                tickerData.append(result)

        print(time.asctime())
        
        for y in tickerData:
            d.write(str(y) + '\n')
            if y != None and y != 'hp':
                f.write(str(y) + '\n')

        print('competed getting data')

        f.close()
        d.close()

        if listCount == 0:
            new = tickerData
            listCount += 1
        elif listCount == 1:
            old = new
            new = tickerData
            listCount += 1
        elif listCount == 2:
            oldest = old
            old = new
            new = tickerData
            listCount += 1
        elif listCount == 3:
            oldest = old
            old = new
            new = tickerData

        if listCount != 3:
            time.sleep(60)
        else:
            time.sleep(1800)

if __name__ == '__main__':
    running = True
    main()


