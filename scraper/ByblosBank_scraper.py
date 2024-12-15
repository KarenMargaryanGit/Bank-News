import requests
from bs4 import BeautifulSoup
import time
import re
import json
from collections import OrderedDict
from datetime import datetime


def update_ByblosBank_news():
    print("--------------------------------------------------")
    print("Starting to update ByblosBank news")
    
    url = 'https://www.byblosbankarmenia.am/en/mediaCenter/all/page'
    url1 = 'https://www.byblosbankarmenia.am'
    news_urls = []
    data = OrderedDict()
    path = 'news/byblosbank_news.json'


    try:
        with open(path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f, object_pairs_hook=OrderedDict)
    except FileNotFoundError:
        existing_data = OrderedDict()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    links = soup.select('.btn-link')
    # print("Links:", links)

    for link in links:
        if link.get('href'):
            if not url1+link.get('href') in existing_data:
                news_urls.append(url1+link.get('href'))
    
    time.sleep(1)

    for url in news_urls:
        try:
            print("--------------------------------------------------")
            print(f"Scraping URL: {url}")

            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title_en = soup.select_one('.news_inner_title').text.strip()
            print(f"Title: {title_en}")

            date = soup.select('.text.text-14.font-spacing-1')[0].text
            day, month, year = date.split('.')[:3]
            formatted_date = f'{year.strip()}-{month.strip()}-{day.strip()}'
            print(f"Date: {formatted_date}")

            content_en = soup.select('.content_text')[1].text.strip()
            content_en = re.sub(r'\n+', ' ', content_en)
            content_en = re.sub(r'\r', ' ', content_en)
            # print(f"content_en length: {len(content_en)} characters")
            
            category = soup.select('.text.text-14.font-uppercase.font-spacing-1.color-gold')[0].text.strip()
            print(f"Category: {category}")

            url_entry = {
                "date": formatted_date,
                "category": category,
                "title_en": title_en,
                "content_en": content_en,
                "title": '',
                "content": '',
                "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            data[url] = url_entry
        
        except Exception as e:
            print(f"Error scraping {url}: {e}")
        
        time.sleep(1)

    data = OrderedDict(sorted(data.items(), key=lambda x: datetime.strptime(x[1]['date'], "%Y-%m-%d"), reverse=True))
    new_data_len = len(data)
    final_data = data

    final_data.update(existing_data)
    print("--------------------------------------------------")
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=4, ensure_ascii=False)
        
        print(f"Total entries: {len(final_data)}")
        print(f"New entries: {new_data_len}")
        print("Done updating Byblos Bank news")
    except Exception as e:
        print(f"Error saving data to {path}: {e}")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)
        
        print(f"Total entries: {len(existing_data)}")
        print("Done updating Byblos Bank news")