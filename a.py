from bs4 import BeautifulSoup
import requests

website_link = "http://today.kz"
today_response = requests.get(website_link)  # С помощью пакета requests парсим всю страницу
today_html = today_response.text # берем текстовую версию response-a(ответ-код)

soup = BeautifulSoup(today_html, 'html.parser') # потом вставляем в bs4

today_news = soup.find("ul", {"class" : "news_list"}) # парсим элементы с типом - 'ul' и в которых аттрибут 'class' равен "news_list"
sub_soup = BeautifulSoup(str(today_news), 'html.parser')  # today_news нужен нам в виде строки и обратно вставляем в bs4

all_links = sub_soup.find_all('a') # здесь из того списка нам нужно вытащить именно ссылки

# <a href = "ssylka"> пример элемента ссылки </a>
for link in all_links[:10]: # берем первые 10 ссылок
    new_link = link['href']    # в тэгах типа 'a', сама ссылка хранится в аттрибуте 'href'
    new_response = requests.get(website_link+new_link) # new_link выглядит примерно так: "news/kazahstan/2017-05-18/742556-kakie-mirovyie-zvezdyi-priedut-na-expo-2017-v-astanu/"
    new_html = new_response.text # обратно запрашиваем весь код страницы этой новости

    new_soup = BeautifulSoup(new_html, 'html.parser')
    new_content = new_soup.find('div', {'class' : 'article_read'}) # находим ту часть кода, в котором нужные нам данные
    #print(new_content) # тектсовый вариант нужной части

    new_soup = BeautifulSoup(str(new_content), 'html.parser')

    new_headline = new_soup.find('h1', {'itemprop' : 'headline'}).text
    print("Заголовок:", new_headline)

    new_image = new_soup.find('div', {'itemprop': 'image'}).img['src']
    print("Фото:",website_link+new_image)

    new_publish_date = new_soup.find('span', {'itemprop': 'datePublished'}).text
    print("Дата публикации:", new_publish_date)

    new_views = new_soup.find('span', {'class': 'view'}).text
    new_comments_number = new_soup.find('span', {'class': 'comment'}).text
    print("Просмотры: %s, Количество комментариев: %s"% (new_views, new_comments_number))

    print("Содержание новости:", end='')
    news_text = new_soup.find('div', {'class': 'text'})
    for paragraph in news_text:
        print(paragraph)

    print('_________________________________________________________________________________________')
