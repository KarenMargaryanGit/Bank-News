import requests
from bs4 import BeautifulSoup
import time
import re
import json
from collections import OrderedDict
from datetime import datetime


def update_ArmEconom_news():
    print("--------------------------------------------------")
    print("Starting to update ArmEconom Bank news")

    url = "https://www.aeb.am/ajax.php"
    url1 = 'https://www.aeb.am/'
    news_urls = []
    data = OrderedDict()
    path = 'news/armeconom_news.json'
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f, object_pairs_hook=OrderedDict)
    except FileNotFoundError:
        existing_data = OrderedDict()

    payload = {
        "start_point": 0,
        "command": "add_news",
        "limit": 900,
        "current_lang_id": 1
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.post(url, data=payload)

        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = soup.find_all('div', class_='news')
    except:
        news_items = []

    for item in news_items:
        link = url1 + item.find('a', class_='title custom_headline')['href']       
        if link in existing_data:
            break
        news_urls.append(link)


    for url in news_urls:
        try:
            print("--------------------------------------------------")
            print(f"Scraping URL: {url}")

            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title = soup.select_one('.news_inner__carousel_item__caption .custom_headline').text.strip()
            print(f"Title: {title}")

            date = soup.select_one('.inner_txt .date').text.strip()
            day, month, year = date.split('.')
            formatted_date = f'{year}-{month}-{day}'
            print(f"Date: {formatted_date}")

            content = soup.select_one('.text-justify').text.strip()
            content = re.sub(r'\n+', '\n', content)
            content = content.replace('\r', ' ')
            # print(f"Content length: {len(content)} characters")

            category = ""
            print(f"Category: {category}")
            url_entry = {
                "date": formatted_date,
                "category": category,
                "title": title,
                "content": content,
                "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            data[url] = url_entry
        
        except Exception as e:
            print(f"Error scraping {url}: {e}")
        
        time.sleep(1)
    
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
        print("Done updating ArmEconom Bank news")
    except Exception as e:
        print(f"Error saving data to {path}: {e}")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)
        
        print(f"Total entries: {len(existing_data)}")
        print("Done updating ArmEconom Bank news")
