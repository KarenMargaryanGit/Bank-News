import requests
from bs4 import BeautifulSoup
import time
import re
import json
from collections import OrderedDict

def update_Ararat_news():
    print("--------------------------------------------------")
    print("Starting to update Ararat news")

    url = 'https://www.araratbank.am/hy/norutyunner/?page=1'
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

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }

            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title = soup.select_one('.static-content h1').text.strip()
            print(f"Title: {title}")

            date = soup.select_one('.inner-box__date').text
            day, month, year = date.split('.')
            formatted_date = f'{year}-{month}-{day}'
            print(f"Date: {formatted_date}")

            content = soup.select_one('.static-content').text.replace(title,"").replace(date,"").strip()
            content = re.sub(r'\n+', '\n', content)
            content = content.replace('\r', ' ')
            # print(f"Content length: {len(content)} characters")
            try:
                category = soup.select_one('.inner-box__link-inner').text.strip()
            except:
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

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }

            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title = soup.select_one('.static-content h1').text.strip()
            print(f"Title: {title}")

            date = soup.select_one('.main-list__date').text
            day, month, year = date.split('.')
            formatted_date = f'{year}-{month}-{day}'
            print(f"Date: {formatted_date}")

            content = soup.select_one('.static-content').text.replace(title,"").replace(date,"").strip()
            content = re.sub(r'\n+', '\n', content)
            content = content.replace('\r', ' ')
            # print(f"Content length: {len(content)} characters")

            category = "Հայտարարություններ"
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
        print("Done updating Ararat announcements")
    except Exception as e:
        print(f"Error saving data to {path}: {e}")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)
        
        print(f"Total entries: {len(existing_data)}")
        print("Done updating Ararat announcements")