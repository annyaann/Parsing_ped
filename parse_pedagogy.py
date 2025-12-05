"""
Мой модуль для парсинга статей по педагогике с сайта pedsovet.org. Извлекает заголовки и ссылки на статьи из карточек на главной странице.
"""

from bs4 import BeautifulSoup
import requests
import json

url = "https://pedsovet.org/"
    
def pedagogika():

    headers = {
        "User-Agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/127.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers = headers, timeout = 10)
        #print(f"Код состояния операции: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при подключении: {e}")
        return ()
            
        
    soup = BeautifulSoup(response.content, 'html.parser')
        
    containers = soup.find_all('div', class_ = 'container')
    
    if not containers:
        print("Ошибка: контейнеры не найдены")
        return ()
       
    k = []

    for i in containers:
        cards = i.find_all('div', class_ = 'cards-unt-item')
        
        for ii in cards:
            tit = ii.find('div', class_ = 'cards-unt-item__title')
            if tit:
                title = tit.get_text()
                title = title.strip()
    
                lin = tit.find('a')
                if lin:
                    link = lin.get('href')

                    if link[0] == '/':
                        link = 'https://pedsovet.org' + link

                    k.append({
                        'Название': title,
                        'Ссылка': link
                    })
    
    return k

result = pedagogika()

if result:

    s = 1

    for i in result:
        print(f"{s}) {i['Название']}")
        print(f"Ссылка: {i['Ссылка']}")
        s += 1
    try:
        with open('articles.json', mode = 'w', encoding = 'utf-8') as file:
            json.dump(result, file, ensure_ascii = False, indent = 2)
    except Exception as e:
            print(f"Ошибка при сохранении: {e}")
