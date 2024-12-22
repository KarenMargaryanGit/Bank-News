import requests
from bs4 import BeautifulSoup
import time
import re
import json
from collections import OrderedDict
from datetime import datetime


def update_AMX_news():
    print("--------------------------------------------------")
    print("Starting to update AMX news")
    url = 'https://amx.am/api/blogs'
    url1 = 'https://amx.am/am/news/'
    news_urls = []
    data = OrderedDict()
    path = 'news/AMX_news.json'
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f, object_pairs_hook=OrderedDict)
    except FileNotFoundError:
        existing_data = OrderedDict()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    data_ = response.json()

    for i in range(len(data_['data'])):
        link = f"{url1}{data_['data'][i]['slug']}/{data_['data'][i]['id']}"
        if link in existing_data:
            url = None
            break

        try:
            content = BeautifulSoup(data_['data'][i]['description'], "html.parser").get_text(separator="\n", strip=True)
            content = re.sub(r'\n+', '\n', content)
            content = content.replace('\r', ' ')
            content = content.strip()
        
            print("--------------------------------------------------")
            print(f"Scraping URL: {link}")
            news_urls.append(link)
            # print(data_['data'][i]['description'])

            title = data_['data'][i]['title']
            date = data_['data'][i]['created_at'].split(' ')[0]
            category = data_['data'][i]['category']

            print(f"Title: {title}")

            print(f"Date: {date}")

            print(f"Category: {category}")



            data[link] = {
                "date": date,
                "category": category,
                "title": title,
                "title_en": data_['data'][i]['title_en'],
                'content': content,
                'scraped_at': time.strftime("%Y-%m-%d %H:%M:%S"),
            }
        except:
            continue

    # print(data)

    new_data_len = len(data)
    final_data = data
    final_data.update(existing_data)
    # final_data = OrderedDict(sorted(final_data.items(), key=lambda x: datetime.strptime(x[1]['date'], "%Y-%m-%d"), reverse=True))
    print("--------------------------------------------------")
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=4, ensure_ascii=False)
        
        print(f"Total entries: {len(final_data)}")
        print(f"New entries: {new_data_len}")
        print("Done updating AMX news")
    except Exception as e:
        print(f"Error saving data to {path}: {e}")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)
        
        print(f"Total entries: {len(existing_data)}")
        print("Done updating AMX news")