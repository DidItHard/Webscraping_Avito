import random
import time
from multiprocessing import Pool

import requests
import xlsxwriter
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pprint import pprint


def get_html(url):
    ''' Функция, возвращающая html текст по url'''

    # Создаем поддельный user-agent
    ua = UserAgent()

    # Создаем заголовок
    headers = {'User-Agent': ua.random}

    # Делаем запрос
    res = requests.get(url, timeout=5, headers=headers)

    # Вывод html кода
    return res.text


def get_data(url):
    html = get_html(url)
    def parse_spec(spec):
        ''' Находит нужную информацию из описания квартиры '''
        spec = spec.strip().lower()
        result = spec

        if 'площадь' in spec:
            result = float(spec.split(': ')[-1].split("\xa0")[0])

        elif 'этаж' in spec:
            result = [int(i) for i in list(spec.split(': ')[-1].split(' из '))]

        elif 'комнат' in spec:
            result = int(spec.split(': ')[-1])

        elif 'балкон' in spec:
            result = spec.split(': ')[-1]

        return result

    dictionary = {'Общая площадь: ': '-', 'Количество комнат: ': '-', 'Этаж: ': '-',
                  'первый этаж': '-',
                  'последний этаж': '-', 'Балкон или лоджия: ': '-', 'Площадь кухни: ': '-',
                  'кухня/квартира': '-',
                  'цена': '-', 'цена квадратного метра': ''}

    soup = BeautifulSoup(html, 'lxml')

    # Отдельные строки
    address = soup.find('div', class_='item-address').find('span',
                                                           class_='item-address__string').text.strip()
    row_price = soup.find('span', class_='js-item-price').text.strip()
    price = int(''.join(row_price.split()))

    # Группа строк
    lines = soup.find('div', class_='item-params').find_all('li', class_='item-params-list-item')

    # Заполняем словарь группой строк
    for line in lines:
        part1 = line.find('span').text
        part2 = line.text

        if part1 in dictionary.keys():
            dictionary[part1] = parse_spec(part2)

    dictionary['цена'] = price
    try:
        dictionary['кухня/квартира'] = round(
            dictionary['Площадь кухни: '] / dictionary['Общая площадь: '], 2)
    except:
        pass

    dictionary['первый этаж'] = 'да' if dictionary['Этаж: '][0] == 1 else 'нет'
    dictionary['последний этаж'] = 'да' if dictionary['Этаж: '][0] == dictionary['Этаж: '][
        1] else 'нет'
    dictionary['цена квадратного метра'] = round(dictionary['цена'] / dictionary['Общая площадь: '])
    dictionary['Этаж: '] = dictionary['Этаж: '][0]
    dictionary['Адрес'] = address
    dictionary['Ссылка'] = url

    dictionary = {''.join([l for l in key.strip() if l != ':']): str(value) for key, value in
                  dictionary.items()}
    return dictionary


if __name__ == '__main__':
    url = 'https://www.avito.ru/semibratovo/kvartiry/2-k._kvartira_50m_13et._1281950308'
    print(get_data(url))
    # print(get_html(url))
