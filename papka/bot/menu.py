import requests
from bs4 import BeautifulSoup
from db.DataBase import DataAccessObject

#from telegram_bot import Bot
import random


class Menu:
    def __init__(self):
        self.__url = 'https://cubemarket.ru/catalog/kubiki-rubika'
        self.__response = requests.get(self.__url)
        self.__data = BeautifulSoup(self.__response.text, 'html.parser')
        self.__dao = DataAccessObject()

    def parsing_rubiks_cubes(self):
        items = self.__data.find_all('div', class_='item')
        for card in items:
            name = card.find("p", class_='item_name').text
            price = card.find('p', class_='item_price').text.replace(' ', '')
            if '%' in price:
                sale = price[:price.find('%')]
            else:
                sale = 0
            price = price[price.find('%') + 1:]
            photo_url = card.find('img').get("src")
            url = card.find('a').get("href")
            url = 'https://cubemarket.ru' + url
            DataAccessObject().insert(name, price, photo_url, url, sale)

    def output(self, new_result):
        for stroke in new_result:
            print(f"Товар: {stroke[0]}. Стоимость товара: {stroke[1]}, URL Фото: {stroke[2]}, URL: {stroke[3]}, Скидка: {stroke[4]}")

    def get_concrete_cube(self, criteria):
        temp = self.__dao.fetchall()
        save = []
        for item in temp:
            if criteria in item[0]:
                save.append(item)
        return save

    def get_max_cube(self):
        return self.__dao.get_max_cube()

    def get_concrete_cube_by_price(self, price_min, price_max):
        return self.__dao.find_concrete_cube_by_price(price_min, price_max)


    def set_url(self, url):
        self.__url = url

    def refresh_data(self):
        self.__data = BeautifulSoup(self.__response.text, 'html.parser')

    def refresh_response(self):
        self.__response = requests.get(self.__url)

    def go_to_new_page(self, url):
        self.set_url(url)
        self.refresh_response()
        self.refresh_data()

    def get_url(self):
        return self.__url

    def get_response(self):
        return self.__response

    def get_html_text(self):
        return BeautifulSoup(self.get_response().text, 'html.parser')

menu = Menu()

menu.parsing_rubiks_cubes()
menu.go_to_new_page("https://cubemarket.ru/catalog/kubiki-rubika?page=2")
menu.parsing_rubiks_cubes()
menu.go_to_new_page("https://cubemarket.ru/catalog/kubiki-rubika?page=3")
menu.parsing_rubiks_cubes()
menu.output(menu.get_max_cube())
print('-')
menu.output(menu.get_concrete_cube_by_price(50, 25000))