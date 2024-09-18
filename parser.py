def scrape_lenta_archive(start_date, end_date):
    base_url = "https://lenta.ru/rubrics/economics/"
    current_date = start_date
    articles = []
    while current_date <= end_date:
        # Формируем URL для текущей даты
        date_url = current_date.strftime("%Y/%m/%d")
        url = base_url + date_url
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Извлекаем все ссылки на статьи на странице
            links = soup.find_all('li', class_='archive-page__item _news')
            for link in links:
                article_url = link.find('a')['href']
                article_response = requests.get(f'https://lenta.ru/{article_url}')
                if article_response.status_code == 200:
                    article_soup = BeautifulSoup(article_response.text, 'html.parser')
                    # Извлекаем заголовок и текст статьи
                    title = article_soup.find('span', class_='topic-body__title')
                    text_title = str(title.text.strip()) if title else ""
                    text_blocks = article_soup.find_all('p', class_='topic-body__content-text')
                    text = ' '.join([block.text.strip() for block in text_blocks])
                    datatime = soup.find("time", {"class": "card-full-news__info-item card-full-news__date"}).text
                    second_value = datatime.split(',')[1].strip()
                    articles.append({'title': text_title, 'text': text, 'datetime': second_value})
        # Переходим к следующей дате
        current_date += timedelta(days=1)
    return articles

# Укажем период времени, за который хотим собрать новости
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 1, 31)

# Получим все статьи за указанный период времени
articles = scrape_lenta_archive(start_date, end_date)

# Выведем количество собранных статей
print("Количество собранных статей:", len(articles))


import json
# Укажем имя файла для записи данных
output_file = "lenta_economics_articles_february.json"

# Записываем статьи в файл JSON
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=4)

print(f"Данные успешно записаны в файл: {output_file}")
