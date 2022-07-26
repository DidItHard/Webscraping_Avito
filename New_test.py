import Create_list_Avito
from datetime import datetime
import csv
from Flat_page import get_html, get_data
from Parsing_name import parsed_address
from Filling_forms import advanced_search
from Parsing_house import parser_house


def open_csv_file(path='result.csv'):
    # Стираем старое содержимое и записывает заголовок
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


def write_data_to_csv(all_data, path='result.csv'):
    '''Записывает данные в csv'''
    try:
        with open(path, "a", newline='', encoding='utf-8') as out_file:
            writer = csv.DictWriter(out_file, delimiter=';', fieldnames=list(all_data.keys()))
            writer.writerow(all_data)
        print('- written successfully')
    except Exception as E:
        print(f'- written failed: {E.__class__.__name__}')


def how_much_time(func):
    # Выводит колво затраченного времени на выполнение кода (декоратор)
    def the_all_func(url):
        t1 = datetime.now() # Запуск замера времени выполнения
        func(url)
        print(f'- Время выполнения: {datetime.now() - t1}')  # Замер времени выполнения
    return the_all_func

# Заполняет flats.txt ссылками с авито
# Create_list_Avito.create_list_links_to_flats('https://www.avito.ru/yaroslavskaya_oblast/kvartiry')

@how_much_time
def all_process_for_one_flat(url):
    ''' Получение всех нужных данных об ОДНОЙ квартире от начальной ссылки с Авито '''
    Flat_data = get_data(url.strip())  # Обрабатываем страницу с квартирой
    print(Flat_data) #!!!!!!!!!!!!!

    # Находим адресс квартиры и форматируем в нужный вид
    address_list_to_search = list(parsed_address(address=Flat_data['Адрес'], link=url).values())

    try:  # Проверка на полноту данных об адреме
        assert None not in address_list_to_search
    except AssertionError:
        print('--- Неправильный адресс или его отсутствие:', address_list_to_search)
        return
    else:
        print('--- Какая-то дичь с форматированием адреса(')
    print(address_list_to_search) #!!!!!!!!!!!!!!!!!


    link_house_to_ReformaJKH = advanced_search(address_list_to_search)  # Ссылка на дом
    House_data = parser_house(link_house_to_ReformaJKH)  # Данные о доме
    print(House_data) #!!!!!!!!!!!!!!!!!

    output_data = {**Flat_data, **House_data}   # Все данные вместе на выход
    return output_data


if __name__ == '__main__':
    flats = [url.strip() for url in open('flats.txt', 'r').readlines()[:4]]
    open_csv_file() # Стираем файл и записываем заголовок

    # Цикл
    # for flat in flats: # Перебираем доступные квартиры
    #     data = all_process_for_one_flat(flat) # Исполняем
    #
    #     write_data_to_csv(data) # Записываем

    data = all_process_for_one_flat(flats[3])  # Исполняем

    write_data_to_csv(data)  # Записываем
