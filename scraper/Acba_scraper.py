import requests
from bs4 import BeautifulSoup
import time
import re
import json
from collections import OrderedDict

def update_Acba_news():
    print("--------------------------------------------------")
    print("Starting to update Acba news")

    url = 'https://www.acba.am/en/news/page/1'
    news_urls = []
    data = OrderedDict()
    path = 'news/acba_news.json'

    try:
        with open(path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f, object_pairs_hook=OrderedDict)
    except FileNotFoundError:
        existing_data = OrderedDict()

    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.select('.item__tpl1__title')

        url_ = soup.select('.pagination a')
        url = None
        for i in range(len(url_)):
            # print(url_[i].get('href'))
            if url_[i].get('class') == ['selected']:
                if i+1 < len(url_):
                    # print(url_[i+1].get('href'),'-----------------')
                    url = 'https://www.acba.am/'+url_[i+1].get('href')
                else:
                    url = None
                break




        for link in links:
            if link.get('href'):
                if 'https://www.acba.am/'+link.get('href') in existing_data:
                    url = None
                    break
                # print(link.get('href'))
                news_urls.append('https://www.acba.am/'+link.get('href'))
        
        # url = None
        time.sleep(1)
    
    for url in news_urls:
        try:
            print("--------------------------------------------------")
            print(f"Scraping URL: {url}")
            url_arm = url
           

            response = requests.get(url_arm)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title_en = soup.select_one('.news_inner__title').text.strip()
            print(f"Title: {title_en}")

            date = soup.select_one('.news_inner__date').text
            # day, month, year = date.split('.')
            # formatted_date = f'{year}-{month}-{day}'
            formatted_date = date
            print(f"Date: {formatted_date}")

            content_en = soup.select_one('.news_inner__text').text.strip()
            content_en = re.sub(r'\n+', '\n', content_en)
            # print(f"Content length: {len(content)} characters")
            try:
                category = soup.select_one('.template_head__title').text.strip()
            except:
                category = ""
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
            
            data[url_arm] = url_entry
        
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
        print("Done updating Acba news")
    except Exception as e:
        print(f"Error saving data to {path}: {e}")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)
        
        print(f"Total entries: {len(existing_data)}")
        print("Done updating Acba news")
