import requests
from bs4 import BeautifulSoup
import time
import re
import json
from collections import OrderedDict
from datetime import datetime


def update_Ineco_news():
    print("--------------------------------------------------")


    url = 'https://www.inecobank.am/api/data/Ineconews?locale=hy&type=internal&orderDirection=DESC&orderBy=Ineconews.date&offset=21&limit=10'

    headers = {
        'Cache-Control': 'no-cache',  # Avoid using cached data
        'If-None-Match': '',  # To force the server to send fresh content
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    cookies = {
        '_ga': 'GA1.1.1533046842.1719865519', 
        'cf_clearance': '...your_cookie_value...',
        # Add any other relevant cookies
    }

    # Sending the GET request
    response = requests.get(url, headers=headers, cookies=cookies)

    # Output the response
    print("Status Code:", response.status_code)


    return








    print("Starting to update Ineco Bank news")
    url = 'https://www.inecobank.am/api/data/Ineconews?locale=hy&orderDirection=DESC&orderBy=Ineconews.date&offset=11&limit=20'
    # url = 'https://www.inecobank.am/hy/Individual/news/details/inecobank-your-business'
    url1 = 'https://www.inecobank.am/hy/Individual/news/details/'
    news_urls = []
    data = OrderedDict()
    path = 'news/ineco_news.json'

    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f, object_pairs_hook=OrderedDict)
    except FileNotFoundError:
        existing_data = OrderedDict()

    url = f"https://www.inecobank.am/api/data/Ineconews"
    
    params = {
        'locale': 'hy',
        'orderDirection': 'DESC',
        'orderBy': 'Ineconews.date',
        'offset': 0,
        'limit': 11
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'https://www.inecobank.am/',
        'Origin': 'https://www.inecobank.am',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
    }
    with requests.Session() as session:
            
        response = session.get(url, headers=headers, timeout=15)
        print(f"Status Code: {response.status_code}")

    # response = requests.get(url, headers=headers, params=params)
    print(response)
    return
    data_ = response.json()


    # print(len(data_))
    for i in range(len(data_)):
        link = f"{url1}{data_[i]['titleInUrl']}"
        print("--------------------------------------------------")
        print(f"Scraping URL: {link}")

        if link in existing_data:
            break
        date = data_[i]['date'].split()[0]
        
        category = ''
        title = data_[i]['headLine']
        content = data_[i]['story']
        summary = data_[i]['summary']

        data[link] = {
                "date": date,
                "category": category,
                "title": title,
                'content': content,
                'summary': summary,
                "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            }

        print(f"Title: {title}")

        print(f"Date: {date}")

        print(f"Category: {category}")

        if i == 5:
            break

    
    new_data_len = len(data)
    final_data = data
    final_data.update(existing_data)
    final_data = OrderedDict(sorted(final_data.items(), key=lambda x: datetime.strptime(x[1]['date'], "%Y-%m-%d"), reverse=True))
    print("--------------------------------------------------")
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=4, ensure_ascii=False)
        
        print(f"Total entries: {len(final_data)}")
        print(f"New entries: {new_data_len}")
        print("Done updating Ineco Bank news")
    except Exception as e:
        print(f"Error saving data to {path}: {e}")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)
        
        print(f"Total entries: {len(existing_data)}")
        print("Done updating Ineco Bank news")