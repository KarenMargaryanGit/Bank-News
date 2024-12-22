import requests
from bs4 import BeautifulSoup
import time
import re
import json
from collections import OrderedDict
from datetime import datetime


def update_AMIO_news():
    print("--------------------------------------------------")
    print("Starting to update Amio Bank news")
    url = '/news?page=1'
    url1 = 'https://amiobank.am'
    news_urls = []
    data = OrderedDict()
    path = 'news/amio_news.json'


    try:
        with open(path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f, object_pairs_hook=OrderedDict)
    except FileNotFoundError:
        existing_data = OrderedDict()

    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    response = requests.get(url1 + url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.select('a[target="_self"]')

    for link in links:
        if link.get('href'):
            if url1+link.get('href') in existing_data:
                continue
        news_urls.append(url1 + link.get('href'))


    while url:

        response = requests.get(url1 + url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.select('.css-1u54fn0')

        
        if links:
            url = url.split('page=')[0] + 'page=' + str(int(url.split('page=')[1]) + 1)
        else:
            url = None

        for link in links:
            if link.get('href'):
                if url1+link.get('href') in existing_data:
                    url = None
                    break
            
                news_urls.append(url1 + link.get('href'))

        # url = None
        time.sleep(1)
    

    for url in news_urls:
        try:
            print("--------------------------------------------------")
            print(f"Scraping URL: {url}")
            
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.select('.chakra-text.css-ff146t')[0].text.strip()
            print(f"Title: {title}")

            date = soup.select_one('.chakra-text.css-4du702').text.strip()
            day, month, year = date.split('.')
            formatted_date = f"{year}-{month}-{day}"
            print(f"Date: {formatted_date}")

            # content = soup.select('.text-guide')[1].text.strip()
            content = soup.select(".chakra-stack.css-153vwuu")[0].text.strip()
            content = re.sub(r'\n+', '\n', content)
            content = content.replace('\r', ' ')
            content = content.strip()
            # print(f"Content length: {len(content)} characters")

            category = ''
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
        print("Done updating Amio news")
    except Exception as e:
        print(f"Error saving data to {path}: {e}")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)
        
        print(f"Total entries: {len(existing_data)}")
        print("Done updating Amio news")