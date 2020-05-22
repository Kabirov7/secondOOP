import mysql.connector
import requests
from bs4 import BeautifulSoup
from parser import Parser

class serials(Parser):
    def change_const(self):
        self.URL = 'http://timemovie.ru/top-100-serialy'
        self.name_table = 'serials'
        self.pages_count = 0

        return self.URL, self.name_table, self.pages_count

    def get_content(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.items = self.soup.find_all('li', class_='serial_x')

        self.content = []
        for self.i in self.items:
            self.content.append({
                'title': self.i.find('a').get_text(),
                'description': 'no description',
                'producer': 'no producer',
                'link': self.i.find('a').get('href')
            })
        return self.content