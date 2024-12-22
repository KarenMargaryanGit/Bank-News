import requests
from bs4 import BeautifulSoup
import time
import re
import json
from collections import OrderedDict
from datetime import datetime


def update_FastBank_news():
    print("--------------------------------------------------")
    print("Starting to update Fast Bank news")
    url = 'https://www.fastbank.am/articles'
    news_urls = []
    data = OrderedDict()
    data_ = OrderedDict()
    path = 'news/fastBank_news.json'

    try:
        with open(path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f, object_pairs_hook=OrderedDict)
    except FileNotFoundError:
        existing_data = OrderedDict()

    while url:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.select('.btn.btn1')

        # url = soup.select_one('.pagination__link--next').get('href') if soup.select_one('.pagination__link--next') else None
        for link in links:
            if link.get('href'):
                if link.get('href') in existing_data:
                    url = None
                    break              
                news_urls.append(link.get('href'))
        
        url = None
        time.sleep(1)
    print(f"Found {len(news_urls)} new news articles")
    return

    for url in news_urls:
        try:
            print("--------------------------------------------------")
            print(f"Scraping URL: {url}")
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }

            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title = data_[url]['title']
            print(f"Title: {title}")

            formatted_date = data_[url]['date']
            print(f"Date: {formatted_date}")

            # content = soup.select('.text-guide')[1].text.strip()
            content = soup.select_one("div.info:has(div.text-guide)").text.strip()
            content = re.sub(r'\n+', '\n', content)
            content = content.replace('\r', ' ')
            content = content.strip()
            # if content.startswith(title):
            #     content = content.replace(title, ' ', 1)
            # print(f"Content length: {len(content)} characters")

            category = url.replace('https://idbank.am/information/about/news/', '').split('/')[0]
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
        print("Done updating Id Bank news")
    except Exception as e:
        print(f"Error saving data to {path}: {e}")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)
        
        print(f"Total entries: {len(existing_data)}")
        print("Done updating Id Bank news")