import requests
from bs4 import BeautifulSoup
import time
import re
import json
from collections import OrderedDict
from translate import translate

def update_Ararat_news():
    print("--------------------------------------------------")
    print("Starting to update Ararat news")

    url = 'https://www.araratbank.am/en/news?page=1'
    news_urls = []
    data = OrderedDict()
    path = 'news/ararat_news.json'

    try:
        with open(path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f, object_pairs_hook=OrderedDict)
    except FileNotFoundError:
        existing_data = OrderedDict()

    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.select('.main-list__link.db')

        url = soup.select_one('.pagination__arrow--next').get('href') if soup.select_one('.pagination__arrow--next') else None

        for link in links:
            if link.get('href'):
                if link.get('href') in existing_data:
                    url = None
                    break
                # print(links[link_index].get('href'))
                news_urls.append(link.get('href'))
        
        # url = None
        time.sleep(1)

    for url in news_urls:
        try:
            print("--------------------------------------------------")
            print(f"Scraping URL: {url}")
            url_arm = url
           

            response = requests.get(url_arm)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title_en = soup.select_one('.static-content h1').text.strip()
            print(f"Title: {title_en}")

            date = soup.select_one('.inner-box__date').text
            day, month, year = date.split('.')
            formatted_date = f'{year}-{month}-{day}'
            print(f"Date: {formatted_date}")

            content_en = soup.select_one('.static-content').text.replace(title_en,"").replace(date,"").strip()
            content_en = re.sub(r'\n+', ' ', content_en)
            # print(f"Content length: {len(content)} characters")
            try:
                category = soup.select_one('.inner-box__link-inner').text.strip()
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
        print("Done updating Ararat news")
    except Exception as e:
        print(f"Error saving data to {path}: {e}")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)
        
        print(f"Total entries: {len(existing_data)}")
        print("Done updating Ararat news")


def update_Ararat_announcements():
    print("--------------------------------------------------")
    print("Starting to update Ararat announcements")

    url = 'https://www.araratbank.am/hy/haytararutyunner?page=1'
    news_urls = []
    data = OrderedDict()
    path = 'news/ararat_announcements.json'

    try:
        with open(path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f, object_pairs_hook=OrderedDict)
    except FileNotFoundError:
        existing_data = OrderedDict()

    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.select('.main-list__link.db.pr')

        url = soup.select_one('.pagination__arrow--next').get('href') if soup.select_one('.pagination__arrow--next') else None

        for link in links:
            if link.get('href'):
                if link.get('href') in existing_data:
                    url = None
                    break
                # print(links[link_index].get('href'))
                news_urls.append(link.get('href'))
        
        # url = None
        time.sleep(1)

    for url in news_urls:
        try:
            print("--------------------------------------------------")
            print(f"Scraping URL: {url}")
            url_arm = url
           

            response = requests.get(url_arm)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title = soup.select_one('.static-content h1').text.strip()
            print(f"Title: {title}")

            date = soup.select_one('.main-list__date').text
            day, month, year = date.split('.')
            formatted_date = f'{year}-{month}-{day}'
            print(f"Date: {formatted_date}")

            content = soup.select_one('.static-content').text.replace(title,"").replace(date,"").strip()
            content = re.sub(r'\n+', ' ', content)
            content = re.sub(r'\r', ' ', content)
            # print(f"Content length: {len(content)} characters")

            category = "announcements"
            print(f"Category: {category}")

            title_en, content_en, _ = translate(title, content,"")

            url_entry = {
                "date": formatted_date,
                "category": category,
                "title_en": title_en,
                "content_en": content_en,
                "title": title,
                "content": content,
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
        print("Done updating Ararat announcements")
    except Exception as e:
        print(f"Error saving data to {path}: {e}")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)
        
        print(f"Total entries: {len(existing_data)}")
        print("Done updating Ararat announcements")