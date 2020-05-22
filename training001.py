import mysql.connector
import requests
from bs4 import BeautifulSoup

class Parser():
    def __init__(self):
        self.URL = ''
        self.HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
           'accept': '*/*'}
        self.DB = mysql.connector.connect(host='localhost', user='root', password='1234', database='films')
        self.MY_CURSOR = self.DB.cursor()
        self.name_table = ''
        self.pages_count = ''
        self.host = ''

    def change_const(self):
        self.URL = ''
        self.name_table = ''
        self.pages_count = ''
        return  self.URL, self.name_table


    def get_html(self, url, params=None):
        self.r = requests.get(url, headers=self.HEADERS, params=params)
        return self.r

    def get_content(self, html):
        pass

    def save_sql(self, items):
        self.MY_CURSOR.execute(f'CREATE TABLE {self.name_table}(ID int PRIMARY KEY AUTO_INCREMENT, title VARCHAR(70), description VARCHAR (250), producer VARCHAR(70), link VARCHAR(130) )')

        for self.i in items:
            self.sqlFormula = f'INSERT INTO {self.name_table}(title, description, producer, link) VALUES (%s,%s,%s,%s)'
            self.films = ([self.i['title'],self.i['description'], self.i['producer'], self.i['link']])
            self.MY_CURSOR.execute(self.sqlFormula, self.films)
        self.DB.commit()

    def main(self):
        self.change_const()
        self.html = self.get_html(self.URL)
        if self.html.status_code == 200:
            self.change_const()
            self.films = []
            for self.page in range(self.pages_count+1):
                print(f'Cтраницы {self.page} из {self.pages_count-1}...')
                self.html = self.get_html(self.URL, params={"page": self.page})
                self.films.extend(self.get_content(self.html.text))
        self.save_sql(self.films)

class kino_afisha(Parser):
    def change_const(self):
        self.URL = 'https://www.kinoafisha.info/rating/movies/'
        self.name_table = 'kino_afisha'
        self.pages_count = 6
        self.host = 'https://www.kinoafisha.info'

        return self.URL, self.name_table, self.pages_count, self.host

    def get_content(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.items = self.soup.find_all('div', class_='films_right')

        self.filmss = []
        for self.i in self.items:
            self.filmss.append({
                'title': self.i.find('a', class_='films_name').get_text(),
                'description': self.host + self.i.find('a', class_='films_name').get('href'),
                'producer': self.i.find_all('span', class_='films_info')[-1].get_text().lstrip('\n').replace(' ', ''),
                'link': 'https://www.google.com/'+ 'смотреть бесплатно 1080p ' + self.i.find('a', class_='films_name').get_text()
            })
        return self.filmss

class netflix(Parser):
    def change_const(self):
        self.URL = 'https://zetflix.cc/serials'
        self.name_table = 'netflix'
        self.pages_count = 17
        self.host = 'https://zetflix.cc'

        return self.URL, self.name_table, self.pages_count, self.host

    def get_content(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.items = self.soup.find_all('div', class_='item')

        self.filmss = []
        for self.i in self.items:
            self.filmss.append({
                'title': self.i.find('div', class_='vid-t').get_text(),
                'description': self.i.find('div', class_='vid-mes').get_text(),
                'producer': 'netflix',
                'link': self.host + self.i.find_previous('a').get('href')
            })
        return self.filmss

class serials(Parser):
    def change_const(self):
        self.URL = 'http://timemovie.ru/top-100-serialy'
        self.name_table = 'serials'
        self.pages_count = 0

        return self.URL, self.name_table, self.pages_count

    def get_content(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.items = self.soup.find_all('li', class_='serial_x')

        self.filmss = []
        for self.i in self.items:
            self.filmss.append({
                'title': self.i.find('a').get_text(),
                'description': 'no description',
                'producer': 'no producer',
                'link': self.i.find('a').get('href')
            })
        return self.filmss


kino_afisha = kino_afisha()
kino_afisha.main()

netflix = netflix()
netflix.main()

serials = serials()
serials.main()