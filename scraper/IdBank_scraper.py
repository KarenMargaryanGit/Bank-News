import requests
from bs4 import BeautifulSoup
import time
import re
import json
from collections import OrderedDict
from datetime import datetime


def update_IdBank_news():
    print("--------------------------------------------------")
    print("Starting to update Id Bank news")
    url = '/information/about/news/'
    url1 = 'https://idbank.am'
    news_urls = []
    data = OrderedDict()
    data_ = OrderedDict()
    path = 'news/idBank_news.json'
    armenian_months = {
        'Հունվար,': '01',
        'Փետրվար,': '02',
        'Մարտ,': '03',
        'Ապրիլ,': '04',
        'Մայիս,': '05',
        'Հունիս,': '06',
        'Հուլիս,': '07',
        'Օգոստոս,': '08',
        'Սեպտեմբեր,': '09',    
        'Հոկտեմբեր,': '10',  
        'Նոյեմբեր,': '11',   
        'Դեկտեմբեր,': '12' 
    }

    try:
        with open(path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f, object_pairs_hook=OrderedDict)
    except FileNotFoundError:
        existing_data = OrderedDict()

    while url:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url1 + url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.select('.news-list__item')

        url = soup.select_one('.pagination__link--next').get('href') if soup.select_one('.pagination__link--next') else None
        for link_i in range(len(links)):
            link = links[link_i].select_one('.news-list__item-link')
            if link.get('href'):
                if url1+link.get('href') in existing_data:
                    url = None
                    break
                title = links[link_i].select_one('.news-list__item-title').text.strip()
                date = links[link_i].select_one('.news-list__item-date').text.strip()

                mount, day, year = date.split()
                if len(day) == 1:
                    day = f'0{day}'
                formatted_date = f'{year}-{armenian_months[mount]}-{day}'
                url_entry = {
                    "date": formatted_date,
                    "title": title,
                }
            
                data_[url1 + link.get('href')] = url_entry
                news_urls.append(url1 + link.get('href'))
        
        # url = None
        time.sleep(1)
    

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