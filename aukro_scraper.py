#!/usr/bin/env python3

import urllib.request
import csv
import re
from datetime import datetime

# Define the URLs to scrape
broad_url = "https://aukro.cz/vysledky-vyhledavani?sort=endingTime_ASC&text=1000&categoryId=109883"
narrow_url = "https://aukro.cz/lp/bankovky-1000-kc-cnb-30-let-menove-odluky?sort=endingTime:ASC"

# Set the user agent to a regular browser
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

# Make a GET request to the broad search URL
broad_request = urllib.request.Request(broad_url, headers={'User-Agent': user_agent})
with urllib.request.urlopen(broad_request) as response:
    broad_html = response.read().decode('utf-8')

# Extract the broad count value from the HTML (one value)
broad_count_start_index = broad_html.find('<span class="tw-text-primary tw-font-bold">')
broad_count_end_index = broad_html.find('</span>', broad_count_start_index)
broad_count = broad_html[broad_count_start_index:broad_count_end_index].split('>')[-1].replace('\xa0', '')

# remove non-numeric characters
broad_count = ''.join(filter(str.isdigit, broad_count))

# Extract the values of class "buy-price" from the HTML, including the time left in minutes
broad_prices = re.findall(r'(?:přihazuj.{0,90})\s*<p\s+class="buy-price">\s*([\d\s]+)\s*Kč\s*<.*?(?=min.{0,90}).*?(class="time-to-end hidden-min-tablet">\s*(\d+)\s*min)?', broad_html)

filtered_broad_prices = []  # Initialize an empty list to store the filtered prices
for price, time_left in broad_prices:  # Iterate through each price and time_left pair in broad_prices
    if time_left is not None and int(time_left) <= 20:  # Check if time_left is not None and is less than or equal to 20
        filtered_broad_prices.append(re.sub('[^0-9]', '', price))  # If both conditions are met, add the price to the filtered_broad_prices list
broad_prices = filtered_broad_prices  # Update broad_prices to contain only the filtered prices

# Get the count of the prices (should be around 14 of them)
broad_price_count = len(broad_prices)

# Make a GET request to the narrow search URL
narrow_request = urllib.request.Request(narrow_url, headers={'User-Agent': user_agent})
with urllib.request.urlopen(narrow_request) as response:
    narrow_html = response.read().decode('utf-8')

# Extract the narrow count value from the HTML
narrow_count_start_index = narrow_html.find('<span class="tw-text-primary tw-font-bold">')
narrow_count_end_index = narrow_html.find('</span>', narrow_count_start_index)
narrow_count = narrow_html[narrow_count_start_index:narrow_count_end_index].split('>')[-1].replace('\xa0', '')

# remove non-numeric characters
narrow_count = ''.join(filter(str.isdigit, narrow_count))

# Extract the values of class "buy-price" from the HTML, including the time left in minutes
narrow_prices = re.findall(r'(?:přihazuj.{0,90})\s*<p\s+class="buy-price">\s*([\d\s]+)\s*Kč\s*<.*?(?=min.{0,90}).*?(class="time-to-end hidden-min-tablet">\s*(\d+)\s*min)?', narrow_html)

filtered_narrow_prices = []  # Initialize an empty list to store the filtered prices
for price, time_left in narrow_prices:  # Iterate through each price and time_left pair in narrow_prices
    if time_left is not None and int(time_left) <= 20:  # Check if time_left is not None and is less than or equal to 20
        filtered_narrow_prices.append(re.sub('[^0-9]', '', price))  # If both conditions are met, add the price to the filtered_narrow_prices list
narrow_prices = filtered_narrow_prices  # Update narrow_prices to contain only the filtered prices

# Get the count of the prices
narrow_price_count = len(narrow_prices)

# Get the current timestamp in the desired format
timestamp = datetime.now().strftime('%d/%m/%y %H:%M')

# Calculate the average and median of the broad and narrow prices
broad_average = sum(broad_prices) / len(broad_prices) if broad_prices else 0
broad_median = sorted(broad_prices)[len(broad_prices) // 2] if broad_prices else 0
narrow_average = sum(narrow_prices) / len(narrow_prices) if narrow_prices else 0
narrow_median = sorted(narrow_prices)[len(narrow_prices) // 2] if narrow_prices else 0

# Set up the CSV dialect with semicolon delimiter
csv.register_dialect('mydialect', delimiter=';', quoting=csv.QUOTE_MINIMAL)

# Write the data to a CSV file
with open('/volume1/SDILENE/AUKRO1000CZKCNB/search_results.csv', 'a', newline='') as f:
    writer = csv.writer(f, dialect='mydialect')
    writer.writerow([
        timestamp,
        broad_count,
        broad_price_count,
        str(broad_average).replace('.', ','),
        str(broad_median).replace('.', ','),
        narrow_count,
        narrow_price_count,
        str(narrow_average).replace('.', ','),
        str(narrow_median).replace('.', ',')
    ])