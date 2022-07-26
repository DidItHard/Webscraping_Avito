''' Тестирование преобразования адресса квартиры с avito в подходящий для Реформы ЖКХ набор данных.
    Для этого спарсим квартирки, достанем url и их адреса.
    (используем Avito_parsing_bs, Flat_page и сам модуль parsing_name'''

import Create_list_Avito
from multiprocessing import Pool
from Flat_page import get_html, get_data
from parsing_name import parsed_address
from filling_forms import advanced_search
from Parsing_house import parser_house
from time import sleep
import random
import csv
import datetime


def random_delay(t1=0.25, t2=1.5):
    # Случайная задержка
    sleep(round(random.uniform(t1, t2), 2))


def open_output(path='result.csv'):
    # Стираем старое содержимое и записываем заголовок
    with open(path, "w", newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(('Общая площадь', 'Количество комнат', 'Этаж', 'первый этаж',
                         'последний этаж', 'Балкон или лоджия', 'Площадь кухни', 'кухня/квартира',
                         'цена', 'цена квадратного метра', 'Адрес', 'Ссылка', 'Год постройки:',
                         'Год ввода дома в эксплуатацию:', 'Серия, тип постройки здания:',
                         'Тип дома:', 'Дом признан аварийным:', 'наибольшее, ед.',
                         'наименьшее, ед.', 'Количество подъездов, ед.', 'Количество лифтов, ед.',
                         'общее, ед.', 'жилых, ед.', 'нежилых, ед.', 'Кадастровый номер',
                         'Тип перекрытий', 'Материал несущих стен'))


def write_data(data1, data2, path='result.csv'):
    '''Записывает данные в csv'''
    try:
        all_data = {**data1, **data2}
        with open(path, "a", newline='', encoding='utf-8') as out_file:
            writer = csv.DictWriter(out_file, delimiter=';', fieldnames=list(all_data.keys()))
            writer.writerow(all_data)
        print('- written successfully')
    except Exception as E:
        print(f'- written failed: {E.__class__.__name__}')


def operation_with_flat_and_house(url):
    try:
        ''' Находит информацию по всем квартирам [bs4] (нужна многопроцессность) '''
        random_delay()

        # Парсим квартиру
        flat_data = get_data(url.strip())

        ''' Перебирем инфу о квартирах; находим адрес, ссылку; находим ссылку на дом и инфу о нем'''
        try:
            # Вычлиняем адрес квартиры и ссылку на нее
            address, link = flat_data['Адрес'], flat_data['Ссылка']

            # Причесываем адрес (для поиска ссылку на дом)
            combed_address = parsed_address(address=address, link=link)
            assert None not in combed_address

            # Находим ссылку на дом
            link_for_house = advanced_search(list(
                combed_address.values()))

            # Парсим дом
            house_data = parser_house(link_for_house)

            # Теперь все запишем
            write_data(flat_data, house_data)

        except Exception as E:
            print(f'written failed: {E.__class__.__name__}')

    except Exception as E:
        print(f'-Квартира не распарсилась: {E.__class__.__name__}')


def old_main():
    t1 = datetime.datetime.now()
    open_output()
    # Заполняет flats.txt ссылками с авито
    # Avito_parsing_bs.main(url='https://www.avito.ru/rossiya/kvartiry/prodam-ASgBAgICAUSSA8YQ', pages=2)

    ''' Находит информацию по всем квартирам [bs4] (нужна многопроцессность) '''
    archive = []  # Информация о всех квартирах
    with open('flats.txt') as file:

        # Перебираем ссылки на квартиры
        for url in file.readlines()[:5]:
            try:
                # Случайная задержка
                sleep(round(random.uniform(0.25, 1.5), 2))

                # Начало времени парсинга
                start = datetime.datetime.now()
                # Парсим квартиру
                flat_data = get_data(url.strip())

                # Сохраняем данные
                archive.append(flat_data)
                print(f'-flat have parsed ({(datetime.datetime.now() - start).seconds} seconds)')

            except Exception as E:
                print(f'-Квартира не распарсилась: {E.__class__.__name__}')

    ''' Перебирем инфу о квартирах; находим адрес, ссылку; находим ссылку на дом и инфу о нем'''
    for i, flat_data in enumerate(archive):
        try:
            # Вычлиняем адрес квартиры и ссылку на нее
            address, link = flat_data['Адрес'], flat_data['Ссылка']

            # Причесываем адрес (для поиска ссылку на дом)
            combed_address = parsed_address(address=address, link=link)

            # Находим ссылку на дом
            link_for_house = advanced_search(list(
                combed_address.values()))

            # Парсим дом
            house_data = parser_house(link_for_house)

            # Теперь все запишем
            write_data(flat_data, house_data)

        except Exception as E:
            print(f'written failed (квартира {i + 1}): {E}')

    # Конечное время выполнения
    print(f'\n---Время выполнения: {(datetime.datetime.now() - t1).seconds} сек')


def main2_0():
    open_output()

    urls = [line.strip() for line in open('flats.txt').readlines()[2:3]]

    with Pool(1) as p:
        p.map(operation_with_flat_and_house, urls)


if __name__ == '__main__':
    t1 = datetime.datetime.now()

    # main2_0()
    operation_with_flat_and_house(
        'https://www.avito.ru/krasnodar/kvartiry/2-k_kvartira_50_m_34_et._2072247762')

    # Конечное время выполнения
    print(f'\n---Время выполнения: {(datetime.datetime.now() - t1).seconds} сек')
