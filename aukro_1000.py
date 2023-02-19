#!/usr/bin/env python3

import urllib.request
import urllib.parse
import csv
import re
import json
import time
from datetime import datetime, timedelta, timezone

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
QUEUE_CHECK_INTERVAL = 1 # v sekundách
REFRESH_QUEUE_LOOP_COUNTER = 3600 # interval = QUEUE_CHECK_INTERVAL * REFRESH_QUEUE_LOOP_COUNTER


queue = []

def addToQueue(item):
    global queue
             
    # vyhodím existující aukci
    queue = list(filter(lambda x: x['item']['itemId'] != item['itemId'], queue))
    # doplním do fronty
    queue.append({
        "id": item["itemId"],
        "item": item,
        "time": datetime.fromisoformat(item["endingTime"]) + timedelta(seconds=1) # TODO nastavit za jak dlouho se mají stabovat poukončení aukce (třeba hours=1)
        })

def sortQueue():
    global queue
    queue.sort(key=lambda x: x["time"], reverse=True)
    
def updateAuctionList(): 
    payload = json.dumps(AUKRO_SEARCH_SETTINGS).encode()
    request = urllib.request.Request(url=AUKRO_API_URL, method='POST', headers={'User-Agent': USER_AGENT, 'Referer': AUKRO_REFERER, 'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json'}, data=payload) 
    with urllib.request.urlopen(request) as response:
        data = json.loads( response.read().decode('utf-8') )
        
        for item in data['content']:
            # TODO přidat za jaké podmínky se má aukce stahovat (např že to je aukce a není to jen buyNow)
            addToQueue(item)

        
def scrapeFinishedAuction(item):
    # TODO dopsat si ukládání do csv
    print(f"screjpuju aukci {item['itemId']}")

    # 1 sestavit url
    # 2 stáhnout html
    # 3 vyparsovat hodnoty jako je částka atd (viz původní scrapper)
    # 4 uložit do jediného řádku csv (viz původní scrapper)
    # 5 projít tenhle soubor a nastavit si hodnoty, kde je TODO a konstanty

def resolveQueue():
    global queue
    
    now = datetime.now().replace(tzinfo=timezone( timedelta(hours=1) ))
    for item in queue:
        if item['time'] < now:
            print(now, item['time']);
            scrapeFinishedAuction(item['item'])
            queue.remove(item)
        


# Hlavní program a smyčka
updateAuctionList()

counter = 0
while(True):
    global L

    counter = counter + 1
    resolveQueue()

    if counter >= REFRESH_QUEUE_LOOP_COUNTER:
        updateAuctionList()
        counter = 0

    time.sleep(QUEUE_CHECK_INTERVAL)

