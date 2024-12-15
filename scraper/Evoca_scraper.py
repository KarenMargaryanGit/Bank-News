import requests
from bs4 import BeautifulSoup
import time
import re
import json
from collections import OrderedDict
from translate import translate

def update_Evoca_news():
    print("--------------------------------------------------")
    print("Starting to update Evoca news")

    url = 'https://www.evoca.am/hy/news/archive?page=1'
    news_urls = []
    data = OrderedDict()
    path = 'news/evoca_news.json'

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

        for link_index in range(0,len(links),2):
            if links[link_index].get('href'):
                if links[link_index].get('href') in existing_data:
                    url = None
                    break
                # print(links[link_index].get('href'))
                news_urls.append(links[link_index].get('href'))
        
        # url = None
        time.sleep(1)

    for url in news_urls:
        try:
            print("--------------------------------------------------")
            print(f"Scraping URL: {url}")
            url_arm = url
            try:
                url_en = url.replace("https://www.evoca.am/hy/", "https://www.evoca.am/en/", 1)
                response = requests.get(url_en)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                title_en = soup.select_one('.news-inner__title').text.strip()
                title_en = re.sub(r'\n+', ' ', title_en)
                title_en = re.sub(r'\"', ' ', title_en)
                print(f"Title_en: {title_en}")
                
                content_en = soup.select_one('.static-content.clear-fix').text.strip()
                content_en = re.sub(r'\n+', ' ', content_en)
                content_en = re.sub(r'\"', ' ', content_en)
                # print(f"Content length: {len(content)} characters")

                category = soup.select_one('.news-list__link-cat').text.strip()
                print(f"Category: {category}")

            except Exception as e:
                print(f"Error scraping {url}(en): {e}")
                title_en = ""
                content_en = ""
                category = ""


            response = requests.get(url_arm)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title = soup.select_one('.news-inner__title').text.strip()
            title = re.sub(r'\n+', ' ', title)
            title = re.sub(r'\"', ' ', title)
            print(f"Title: {title}")

            date = soup.select_one('.news-inner__date').text
            day, month, year = date.split('.')
            formatted_date = f'{year}-{month}-{day}'
            print(f"Date: {formatted_date}")

            content = soup.select_one('.static-content.clear-fix').text.strip()
            content = re.sub(r'\n+', ' ', content)
            content = re.sub(r'\"', ' ', content)
            # print(f"Content length: {len(content)} characters")
            
            if category == "":
                category = soup.select_one('.news-list__link-cat').text.strip()
                print(f"Category: {category}")

            if title_en == ""  and content_en == "":
                title_en, content_en, category = translate(title, content, category)

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
        print("Done updating Evoca news")
    except Exception as e:
        print(f"Error saving data to {path}: {e}")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)
        
        print(f"Total entries: {len(existing_data)}")
        print("Done updating Evoca news")



def update_Evoca_announcements():
    print("--------------------------------------------------")
    print("Starting to update Evoca announcements")

    url = 'https://www.evoca.am/hy/announcements?page=1'

    data = OrderedDict()
    path = 'news/evoca_announcements.json'
    category = 'announcements'

    try:
        with open(path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f, object_pairs_hook=OrderedDict)
    except FileNotFoundError:
        existing_data = OrderedDict()

    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.select('.main-list__link')

        url = soup.select_one('.pagination__arrow--next').get('href') if soup.select_one('.pagination__arrow--next') else None

        for link in links:

            title = link.select_one('.accordion__title-text').text.strip()
            title = re.sub(r'\n+', ' ', title)
            title = re.sub(r'\"', ' ', title)
            date = link.select_one('.accordion__date').text.strip()
            if title+'--'+date in existing_data:
                url = None
                break
            
            print("--------------------------------------------------")
            print(f"Title: {title}")


            content = link.select_one('.accordion__content').text.strip()
            content = re.sub(r'\n+', ' ', content)
            content = re.sub(r'\"', ' ', content)
            print(f"Category: {category}")

            day, month, year = date.split('.')
            formatted_date = f'{year}-{month}-{day}'
            print(f"Date: {formatted_date}")

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

            data[title+'--'+date] = url_entry
        
        # url = None
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
        print("Done updating Evoca announcements")
    except Exception as e:
        print(f"Error saving data to {path}: {e}")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)
        
        print(f"Total entries: {len(existing_data)}")
        print("Done updating Evoca announcements")