import mysql.connector
import requests
from bs4 import BeautifulSoup
from parser import Parser

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

        self.content = []
        for self.i in self.items:
            self.content.append({
                'title': self.i.find('a', class_='films_name').get_text(),
                'description': self.host + self.i.find('a', class_='films_name').get('href'),
                'producer': self.i.find_all('span', class_='films_info')[-1].get_text().lstrip('\n').replace(' ', ''),
                'link': 'https://www.google.com/'+ 'смотреть бесплатно 1080p ' + self.i.find('a', class_='films_name').get_text()
            })
        return self.content