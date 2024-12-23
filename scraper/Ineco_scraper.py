import requests
from bs4 import BeautifulSoup
import time
import re
import json
from collections import OrderedDict
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def update_Ineco_news():
    print("--------------------------------------------------")
    print("Starting to update Ineco Bank news")
    url_list = {'https://www.inecobank.am/hy/press-center':'news',
                'https://www.inecobank.am/hy/press-center/announcements?category=customers':'customers',
                'https://www.inecobank.am/hy/press-center/announcements?category=bonds':'bonds',
                'https://www.inecobank.am/hy/press-center/announcements?category=shareholders':'shareholders',
                'https://www.inecobank.am/hy/press-center/announcements?category=authorizedcapital':'authorizedcapital',
                'https://www.inecobank.am/hy/press-center/announcements?category=dividends':'dividends',
                'https://www.inecobank.am/hy/press-center/announcements?category=other2':'other',}
    
    url1 = 'https://www.inecobank.am'
    news_urls = []
    data = OrderedDict()
    path = 'news/ineco_news.json'
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            existing_data = json.load(f, object_pairs_hook=OrderedDict)
    except FileNotFoundError:
        existing_data = OrderedDict()
    
    options = Options()
    options.headless = True
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--disable-gpu")  # Disable GPU (optional)
    options.add_argument("--no-sandbox")  # Prevent the sandbox (optional)

    for url in url_list.keys():
        try:
            driver = webdriver.Chrome( options=options)
            driver.get(url)
            time.sleep(1)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            links = soup.select('div.propertyContentList__listItem div.propertyContentCard__content a.btn__link')
            news_urls = []
            for link in links:
                if link.get('href'):
                    if url1+link.get('href') in existing_data:
                        break
                    news_urls.append(url1+link.get('href'))

            driver.quit()
            category = url_list[url]
            for url in news_urls:
                try:
                    driver = webdriver.Chrome( options=options)
                    print("--------------------------------------------------")
                    print(f"Scraping URL: {url}")
                    driver.get(url)
                    time.sleep(1)
                    page_source = driver.page_source
                    soup = BeautifulSoup(page_source, 'html.parser')

                    title = soup.select_one('.newsPage__title').text.strip()
                    content = soup.select_one(".newsPage__content").text.strip()
                    content = re.sub(r'\n+', '\n', content)
                    content = content.replace('\r', ' ')
                    content = content.strip()
                    date = soup.select_one('.newsPage__date').text.split('.')
                    formatted_date = f"{date[2]}-{date[1]}-{date[0]}"
                    
                    print(f"Title: {title}")
                    print(f"Date: {formatted_date}")
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
                    continue
                finally:
                    driver.quit()
        except:
            continue
    
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
        print("Done updating Ineco Bank news")
    except Exception as e:
        print(f"Error saving data to {path}: {e}")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)
        
        print(f"Total entries: {len(existing_data)}")
        print("Done updating Ineco Bank news")
