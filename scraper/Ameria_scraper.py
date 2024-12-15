import requests
from bs4 import BeautifulSoup
import time
import re
import json
from collections import OrderedDict

def update_Ameria_news():
    print("--------------------------------------------------")
    print("Starting to update Ameria news")
    
    url = 'https://ameriabank.am/media-room/pageindex39221/1'
    news_urls = []
    data = OrderedDict()
    path = 'news/ameria_news.json'
    armenian_months = {
        'Հնվ': '01',
        'Փտվ': '02',
        'Մրտ': '03',
        'Ապր': '04',
        'Մյս': '05',
        'Հնս': '06',
        'Հլս': '07',
        'Օգս': '08',
        'Սպտ': '09',    
        'Հկտ': '10',  
        'Նյմ': '11',   
        'Դկտ': '12' 
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
            url_arm = url
            try:
                url_en = url.replace("https://ameriabank.am/", "https://ameriabank.am/en/", 1)
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                }

                response = requests.get(url_en, headers=headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                title_en = soup.select_one('.detail-title').text.strip()
                print(f"Title_en: {title_en}")
                
                content_en = soup.select_one('.detail-description').text.strip()
                content_en = re.sub(r'\n+', ' ', content_en)
                content_en = re.sub(r'\r', ' ', content_en)
                # print(f"Content length: {len(content)} characters")

                category = soup.select_one('.detail-info').text.split('|')[1].strip()
                print(f"Category: {category}")

            except Exception as e:
                print(f"Error scraping {url}(en): {e}")
                title_en = ""
                content_en = ""
                category = ""

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }

            response = requests.get(url_arm, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title = soup.select_one('.detail-title').text.strip()
            print(f"Title: {title}")

            date = soup.select_one('.detail-info').text
            day, month_armenian, year = date.split()[:3]
            month = armenian_months[month_armenian.split(',')[0]]
            formatted_date = f'{year}-{month}-{day}'
            print(f"Date: {formatted_date}")

            content = soup.select_one('.detail-description').text.strip()
            content = re.sub(r'\n+', ' ', content)
            content = re.sub(r'\r', ' ', content)
            # print(f"Content length: {len(content)} characters")
            if category == "":
                category = soup.select_one('.detail-info').text.split('|')[1].strip()
                print(f"Category: {category}")

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
        print("Done updating Ameria news")
    except Exception as e:
        print(f"Error saving data to {path}: {e}")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)
        
        print(f"Total entries: {len(existing_data)}")
        print("Done updating Ameria news")