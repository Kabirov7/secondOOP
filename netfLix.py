import mysql.connector
import requests
from bs4 import BeautifulSoup
from parser import Parser

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

        self.content = []
        for self.i in self.items:
            self.content.append({
                'title': self.i.find('div', class_='vid-t').get_text(),
                'description': self.i.find('div', class_='vid-mes').get_text(),
                'producer': 'netflix',
                'link': self.host + self.i.find_previous('a').get('href')
            })
        return self.content