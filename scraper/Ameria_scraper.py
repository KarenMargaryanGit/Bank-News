import requests
from bs4 import BeautifulSoup
import time
import re
import json
from collections import OrderedDict

def update_Ameria_news():
    print("--------------------------------------------------")
    print("Starting to update Ameria news")
    url = 'https://ameriabank.am/en/media-room/pageindex39221/1'
    news_urls = []
    data = OrderedDict()
    path = 'news/ameria_news.json'
    armenian_months = {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',    
        'Oct': '10',  
        'Nov': '11',   
        'Dec': '12' 
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

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.select('.list-btn')

        url = soup.select_one('.next').get('href') if soup.select_one('.next') else None

        for link in links:
            if link.get('href'):
                if link.get('href') in existing_data:
                    url = None
                    break
                news_urls.append(link.get('href'))
        
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
            
            title = soup.select_one('.detail-title').text.strip()
            print(f"Title: {title}")

            date = soup.select_one('.detail-info').text
            day, month_armenian, year = date.split()[:3]
            month = armenian_months[month_armenian.split(',')[0]]
            formatted_date = f'{year}-{month}-{day}'
            print(f"Date: {formatted_date}")

            content = soup.select_one('.detail-description').text.strip()
            content = re.sub(r'\n+', '\n', content)
            content = content.replace('\r', ' ')
            # print(f"Content length: {len(content)} characters")

            category = soup.select_one('.detail-info').text.split('|')[1].strip()
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
    print("--------------------------------------------------")
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=4, ensure_ascii=False)
        
        print(f"Total entries: {len(final_data)}")
        print(f"New entries: {new_data_len}")
        print("Done updating Ameria news")
    except Exception as e:
        print(f"Error saving data to {path}: {e}")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)
        
        print(f"Total entries: {len(existing_data)}")
        print("Done updating Ameria news")