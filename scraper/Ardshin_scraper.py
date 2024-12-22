import requests
from bs4 import BeautifulSoup
import time
import re
import json
from collections import OrderedDict
from datetime import datetime


def update_Ardshin_news():
    print("--------------------------------------------------")
    print("Starting to update Ardshin Bank news")
    url = 'https://website-api.ardshinbank.am/pages/page-type/65f96b8bbee4181a44ad83b9'
    url1 = 'https://website-api.ardshinbank.am/pages/alias'
    url2 = 'https://ardshinbank.am'
    news_urls = []
    data = OrderedDict()
    path = 'news/ardshin_news.json'


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


    # print(len(data_))
    for i in range(len(data_)):
        link = f"{url2}{data_[i]['page']['realAlias']}"
        if link in existing_data:
            break
        date = data_[i]['history']['publishDate'].split('T')[0]
        try:
            category = data_[i]['page']['category']
            if not category:
                category = ""
        except:
            category = ''
        title = data_[i]['page']['name']
        content = ''

        data[link] = {
                "date": date,
                "category": category,
                "title": title,
            }
        news_urls.append(link)


    for url in news_urls:
        try:
            print("--------------------------------------------------")
            print(f"Scraping URL: {url}")
            
            # request = requests.get(data[url]['api'], headers=headers).json()['page']['content']
            # if request[2]['props']['659bda51d10aaeb6566397f8']['data']['content']:
            #     content = request[2]['props']['659bda51d10aaeb6566397f8']['data']['content']
            # elif request[1]['props']['659bda51d10aaeb6566397f8']['data']['content']:
            #     content = request[1]['props']['659bda51d10aaeb6566397f8']['data']['content']
            # else:
            #     content = request[-1]['props']['659bda51d10aaeb6566397f8']['data']['content']
            # content = BeautifulSoup(content, "html.parser").get_text(separator="\n", strip=True)

            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            content = soup.select_one('.tw-overflow-x-auto').text

            content = re.sub(r'\n+', '\n', content)
            content = content.replace('\r', ' ')
            content = content.strip() 
            # print("Content len", len(content))

            print(f"Title: {data[url]['title']}")


            print(f"Date: {data[url]['date']}")

            print(f"Category: {data[url]['category']}")
            
            data[url]['content'] = content
            data[url]["scraped_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            
        
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
        print("Done updating Ardshin Bank news")
    except Exception as e:
        print(f"Error saving data to {path}: {e}")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)
        
        print(f"Total entries: {len(existing_data)}")
        print("Done updating Ardshin Bank news")