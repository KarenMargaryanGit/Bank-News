import requests
from bs4 import BeautifulSoup
import time
import re
import json
from collections import OrderedDict
from datetime import datetime


def update_Converse_news():
    print("--------------------------------------------------")
    print("Starting to update Converse Bank news")

    url_announcements = 'https://conversebank.am/hy/announcements/page/1/'
    url1 = 'https://conversebank.am'
    api = 'https://sapi.conversebank.am/api/v2/blogs'
    news_urls = []
    data = OrderedDict()
    path = 'news/converse_news.json'
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f, object_pairs_hook=OrderedDict)
    except FileNotFoundError:
        existing_data = OrderedDict()
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    while url_announcements:
        response = requests.get(url_announcements, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.select('.news-items a')

        try:
            url_announcements = url1 + soup.find('a', string=lambda text: text and "Հաջորդ →" in text).get('href')
        except:
            url_announcements = None

        for link in links:
            if link.get('href'):
                if url1 + link.get('href') in existing_data:
                    url_announcements = None
                    break
                news_urls.append(url1 + link.get('href'))
        time.sleep(1)

    for url in news_urls:
        try:
            print("--------------------------------------------------")
            print(f"Scraping URL: {url}")
            
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title = soup.select_one('.title-nomargin').text.strip()
            print(f"Title: {title}")

            date = soup.select_one('.leg-date').text.split()[-1]
            day, month, year = date.split('.')[:3]
            formatted_date = f'{year}-{month}-{day}'
            print(f"Date: {formatted_date}")

            content = soup.select_one('.news-text').text.strip()
            content = re.sub(r'\n+', '\n', content)
            content = content.replace('\r', ' ')
            # print(f"Content length: {len(content)} characters")

            category = 'announcements'
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

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'hy',
        'origin': 'https://www.conversebank.am',
        'priority': 'u=1, i',
        'referer': 'https://www.conversebank.am/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }
    try:
        for page in [None, 0,1,2,3,4,5,6,7,8,9,]:
            params = {
                'page': page,
            }

            response = requests.get(api, params=params, headers=headers)
            data_ = response.json()
            for i in data_['data']:
                # print(i['id'], i['title'])
                # print(i)
                url = 'https://conversebank.am/blog/item/' + i['slug']
                title = i['title']
                summary = i.get('summary','')
                formatted_date = i['created_at'].split('T')[0]
                content = BeautifulSoup(i['block_banner']['body'], "html.parser").get_text()
                content = re.sub(r'\n+', '\n', content)
                content = content.replace('\r', ' ').strip()

                # print(i['tags'])
                category = i['tags'][0]['title']

                url_entry = {
                    "date": formatted_date,
                    "category": category,
                    "title": title,
                    'summary': summary,
                    "content": content,
                    "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                if url in data or url in existing_data:
                    continue
                print("--------------------------------------------------")
                print(f"Scraping URL: {url}")
                print(f"Title: {title}")
                print(f"Date: {formatted_date}")
                print(f"Category: {category}")
                data[url] = url_entry
                # return
            time.sleep(1)
    except:
        pass

    try:
        for archive in [0,1,2,3,4,5,6,7,8,9,]:
            params = {
                'is_archive': archive,
            }

            response = requests.get(api, params=params, headers=headers)
            data_ = response.json()
            # print(data_)
            for i in data_['data']:
                # print(i['id'], i['title'])
                # print(i)
                url = 'https://conversebank.am/blog/item/' + i['slug']
                title = i['title']
                summary = i.get('summary','')
                formatted_date = i['created_at'].split('T')[0]
                content = BeautifulSoup(i['block_banner']['body'], "html.parser").get_text()
                content = re.sub(r'\n+', '\n', content)
                content = content.replace('\r', ' ').strip()
                try:
                    category = i['tags'][0]['title']
                except:
                    category = ''


                url_entry = {
                    "date": formatted_date,
                    "category": category,
                    "title": title,
                    'summary': summary,
                    "content": content,
                    "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                if url in data or url in existing_data:
                    continue
                print("--------------------------------------------------")
                print(f"Scraping URL: {url}")
                print(f"Title: {title}")
                print(f"Date: {formatted_date}")
                print(f"Category: {category}")
                data[url] = url_entry
            time.sleep(1)
    except:
        pass
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
        print("Done updating Converse Bank news")
    except Exception as e:
        print(f"Error saving data to {path}: {e}")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)
        
        print(f"Total entries: {len(existing_data)}")
        print("Done updating Converse Bank news")
