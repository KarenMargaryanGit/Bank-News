import requests

def translate(title, content, category=""):

    url = "https://google-translate1.p.rapidapi.com/language/translate/v2"


    headers = {
        "x-rapidapi-key": "14cc5e8736msh8c75a54ba3c6bacp1c80f4jsncac5949e9df8", # my account
        # "x-rapidapi-key": "9d22f32413mshdb9880a804a0e23p194114jsn20efbd9b95f5", # other account
        "x-rapidapi-host": "google-translate1.p.rapidapi.com",
        "Accept-Encoding": "application/gzip"
    }

    text_to_translate = [title, content, category]

    data = {
        "q": text_to_translate,          
        "source": "hy",                  
        "target": "en",                  
        "format": "text"
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        translation = response.json()
        title_en = translation["data"]["translations"][0]["translatedText"]
        content_en = translation["data"]["translations"][1]["translatedText"]
        category_en = translation["data"]["translations"][2]["translatedText"]
        # print(f"Translated Text: {translated_text}")
        # print(f"Translated Text: {translated_text_}")
        return (title_en, content_en, category_en)
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return ("","","")


