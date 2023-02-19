#!/usr/bin/env python3

import urllib.request
import urllib.parse
import csv
import re
import json
from datetime import datetime

AUKRO_API_URL = "https://backend.aukro.cz/backend-web/api/offers/searchItemsCommon?page=0&size=180&sort=endingTime:ASC"
AUKRO_SEARCH_SETTINGS = {
    "text":"1000",
    "categoryId":109883,
    "splitGroupKey":"search",
    "splitGroupValue":"D17",
    "fallbackItemsCount":12
    }
AUKRO_REFERER = 'https://aukro.cz/vysledky-vyhledavani?size=120&sort=endingTime_ASC&text=1000&categoryId=109883'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

queue = []
    

def getAuctionList():
    
    payload = json.dumps(AUKRO_SEARCH_SETTINGS).encode()
    request = urllib.request.Request(url=AUKRO_API_URL, method='POST', headers={'User-Agent': USER_AGENT, 'Referer': AUKRO_REFERER, 'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json'}, data=payload)
    
    with urllib.request.urlopen(request) as response:
        data = json.loads( response.read().decode('utf-8') )
        
        for item in data['content']:
            global queue
             
            # vyhodím existující aukci
            queue = list(filter(lambda x: x['itemId'] != item['itemId'], queue))
            # doplním do fronty
            queue.append(item)

        queue.sort(key=lambda x: x["endingTime"], reverse=True)

# Hlavní program
getAuctionList()

print(len(queue))



