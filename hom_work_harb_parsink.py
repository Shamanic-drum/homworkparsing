import requests
from bs4 import BeautifulSoup # pyright: ignore[reportMissingImports]
from datetime import datetime

#список ключевых слов:
KEYWORDS = ['дизайн', 'фото', 'web', 'python']
# URL
URL = 'https://habr.com/ru/articles/'
def fetch_articles(url, keywords):
    """Парсит статьи и возвращает подходящие по ключевым словам"""
    try:
        # Отправляем запрос
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверяем успешность запроса

        # BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        # Находим все статьи (ищем по классу, который содержит превью статьи)
        articles = soup.find_all('article', class_='tm-articles-list__item')
        matching_articles = []
        # поиск
        for article in articles:
            # заголовок
            title_elem = article.find('h2', class_='tm-title')
            if not title_elem:
                title_elem = article.find('a', class_='tm-title__link')
            title = title_elem.text.strip() if title_elem else "Без названия"
            # ссылка
            link_elem = article.find('a', class_='tm-title__link')
            if link_elem and link_elem.get('href'):
                link = 'https://habr.com' + link_elem['href']
            else:
                link = "#"
            # дата
            date_elem = article.find('time')
            if date_elem and date_elem.get('datetime'):
                date = date_elem['datetime'][:10]  # Берем только дату
            else:
                date = datetime.now().strftime('%Y-%m-%d')
            preview_text = ''
            preview_text += title.lower() + ' '
            preview_paragraphs = article.find_all('p')
            for p in preview_paragraphs:
                preview_text += p.text.lower() + ' '
            
            # текст из тегов (хабов)
            tags = article.find_all('a', class_='tm-tags-list__link')
            for tag in tags:
                preview_text += tag.text.lower() + ' '
            is_matching = any(keyword.lower() in preview_text for keyword in keywords)
            
            if is_matching:
                matching_articles.append({
                    'date': date,
                    'title': title,
                    'link': link
                })
        
        return matching_articles
    
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return []
    except Exception as e:
        print(f"Ошибка парсинга: {e}")
        return []

def main():
    print(f"Поиск статей : {', '.join(KEYWORDS)}")
    print("-" * 80)
    articles = fetch_articles(URL, KEYWORDS)
    
    if articles:
        for article in articles:
            print(f"{article['date']} – {article['title']} – {article['link']}")
        print(f"\nНайдено статей: {len(articles)}")
    else:
        print("Статей не найдено, сегодня харберы отдыхают)).")

if __name__ == "__main__":
    main()
