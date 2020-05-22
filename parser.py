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
                self.html = self.get_html(self.URL, params={"page": self.page})
                self.films.extend(self.get_content(self.html.text))
        self.save_sql(self.films)