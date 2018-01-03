#! /usr/local/bin/python3

# Copyright (C) 2017 Brian Hartvigsen, Elijah Hartvigsen
# See LICENSE file for full copyright license details

import csv
import requests
from bs4 import BeautifulSoup

URL = "http://abugames.com/shop.cgi"


def getCardPrices(cardname):
    params = {'command': 'search',
              'log': '1',
              'cardname': cardname,
              'edition': '0',
              'displaystyle': 'list',
              'x': '0',
              'y': '0'}
    # This prints out the raw HTML
    # print(requests.get(url).text)

    soup = BeautifulSoup(requests.get(URL, params=params).text, "lxml")

    prices = {}
    for card in soup.find_all('div', class_='cardinfo'):
        for row in card.find('table', recursive=False).find_all('tr'):
            data = row.find_all('td')
            if len(data) < 4:
                continue
            quality = data[1].a.text
            quantity = int(data[2].text)
            if data[3].find('span'):
                cost = float(data[3].find_all('span')[-1].text[1:])
            else:
                cost = float(data[3].text[1:])
            if quantity == 0:
                continue

            if quality not in prices or prices[quality] > cost:
                prices[quality] = cost
    return prices


with open('/Users/bhartvigsen/Downloads/pricelist.csv', 'a') as wfp:
    csvwriter = csv.writer(wfp)
    with open('/Users/bhartvigsen/Downloads/golden_monkey.txt', 'r') as rfp:
        for line in rfp:
            name = line.strip()
            prices = getCardPrices(name)
            mint_price = prices['(NM-M)'] if '(NM-M)' in prices else 0.00
            play_price = prices['(PLD-SPLD)'] if '(PLD-SPLD)' in prices else 0.00
            print("%s %0.2f %0.2f" % (name, mint_price, play_price))
            csvwriter.writerow([name, mint_price, play_price])
#print(getCardPrices('Elesh Norn, Grand Cenobite'))

# First result, first quality with quantity > 0
