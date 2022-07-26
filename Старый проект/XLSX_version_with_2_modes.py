import random
import time

import requests
import xlsxwriter
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def get_html_map(url):
    ''' Функция, возвращающая html текст '''

    # Создаем поддельный user-agent
    ua = UserAgent()

    # Создаем заголовок
    headers = {'User-Agent': ua.random}

    # Делаем запрос
    res = requests.get(url, timeout=5, headers=headers)

    if res.status_code >= 400 and res.status_code <= 599:
        return False

    # Вывод html кода
    return res.json()


def get_data_map(html):
    ''' Работает с одной страницей. Берет из нее данные по всем квартирам и
    записывает их в xlxs-файл '''

    # Если ошибка
    if not html:
        return False

    flats = html['items']

    # Если квартиры кончились
    if len(flats) == 0:
        return False

    for flat in flats:
        # area = flat['ext']['area']
        price = float(flat['price'])
        meters, name = divider_name(flat['title'])
        url = 'https://avito.ru' + flat['url']
        price_per_meter = int(price / meters)

        # Сохраняем данные в списке.
        data = [name,
                float(price),
                float(meters),
                float(price_per_meter),
                url]

        # Если квартира продается, а не сдается.
        if price_per_meter > 2000:
            global row
            worksheet.set_row(row, 30)

            # Заполняем ячейки
            for col, staff in enumerate(data):
                if col != 5:
                    worksheet.write(row, col, staff, body_format)
                else:
                    worksheet.write(row, col, staff, sink_format)

        row += 1

    return True


def get_html(url):
    ''' Функция, возвращающая html текст '''

    # Создаем поддельный user-agent
    ua = UserAgent()

    # Создаем заголовок
    headers = {'User-Agent': ua.random}

    # Делаем запрос
    res = requests.get(url, timeout=5, headers=headers)

    # Вывод html кода
    return res.text


def get_total_pages(html):
    ''' Возвращает обшее кол-ко доступных страниц'''
    soup = BeautifulSoup(html, 'lxml')

    pages = soup.find('div', class_='pagination-root-2oCjZ').find_all('span')[-2]
    total_pages = str(pages).split()[-1].split('>')[1].split('<')[0]
    return int(total_pages)


def divider_name(s):
    ''' Преобразовывает названия объявлений в нужные нам данные '''
    try:
        lst = s.split(',')
        meters = float(lst.ksdjhfgjk(1).strip().split()[0])
        name = ', '.join(lst)
        return (meters, name)
    except:
        return (0, 0)


def get_data(html):
    ''' Работает с одной страницей. Берет из нее данные по всем квартирам и
    записывает их в xlxs-файл '''

    soup = BeautifulSoup(html, 'lxml')

    # Находим все квартиры
    flats = soup.find_all(class_='item__line')

    # Перебираем квартиры
    for flat in flats:
        name = flat.find('a', class_='snippet-link').text

        # Если название не по формату, то пропускаем эту квартиру.
        # (очень редко и, скорее всего, квартира не на продажу)
        if divider_name(name) != (0, 0):
            # Кол-во метров; 'тип' квартиры (кол-во комнат, этаж)
            meters, name = divider_name(name)
        else:
            continue

        # Есть разные классы названий на Avito (обычные и подсвеченные).
        try:
            price = flat.find('span', class_='snippet-price snippet-price-vas').text
        except:
            price = flat.find('span', class_='snippet-price ').text

        # Цена; url; цена за метр
        price = ''.join(price.strip().split('  ')[0].split())
        url = 'https://www.avito.ru' + flat.find('a', class_='snippet-link').get('href')
        price_per_meter = int(int(price) / int(float(meters)))

        # Сохраняем данные в списке.
        data = [name,
                float(price),
                float(meters),
                float(price_per_meter),
                url]

        # Если квартира продается, а не сдается.
        if price_per_meter > 2000:
            global row
            worksheet.set_row(row, 30)

            # Заполняем ячейки
            for col, staff in enumerate(data):
                if col != 5:
                    worksheet.write(row, col, staff, body_format)
                else:
                    worksheet.write(row, col, staff, sink_format)

        row += 1


def get_town(html, mode='лента'):
    if mode == 'лента':
        soup = BeautifulSoup(html, 'lxml')
        town = soup.find('div', class_='main-text-2PaZG').text

    elif mode == 'карта':
        flat = html['items'][0]
        adress = flat['coords']['address_user'].split(',')[0]
        town = adress.split(',')[0]
    else:
        return '---Город не определен---'

    return town


def main():
    ''' Тело программы '''

    # Если введенные параметры пользователя будут не корректны
    main.stop = False

    mode = input('Выбирите режим — лента(1) или карта(2)?:')
    if mode == '1' or mode == 'лента':
        url = input('Введите url страницы с квартирами Avito (потом пробел и enter): ').strip()
    elif mode == '2' or mode == 'карта':
        url = input(
            'Введите Request URL страницы с квартирами Avito (потом пробел и enter): ').strip()
    else:
        print('\n(Режим программы не выбран.)')
        # Конечные данные не сохранятся
        main.stop = True
        return

    # Если недобропорядочный пользователь подсунул не страницу Avito.
    if 'www.avito' not in url:
        if mode == '1' or mode == 'лента':
            print('\nЭто не страница Avito!')
        elif mode == '2' or mode == 'карта':
            print('\nЭто не XHR запрос на сервер Авито!')

        # Конечные данные не сохранятся
        main.stop = True
        return

    # Если режим ленты
    if mode == '1' or mode == 'лента':
        # Ввод кол-во страниц, которые пользователь хочет обработать.
        try:
            str_user_pages = input('Введите кол-во страниц для сбора данных: ')
            user_pages = int(str_user_pages)
        except:
            # Если пользователь нажал только enter
            if not str_user_pages:
                user_pages = 1
            else:
                print('\nВведенное кол-во страниц не является целым числом!')

                # Конечные данные не сохранятся
                main.stop = True
                return

    # Формат первоначальной записи
    tittle_format = workbook.add_format()
    tittle_format.set_font_script()
    tittle_format.set_font_size(30)
    tittle_format.set_bold()
    tittle_format.set_align('right')
    tittle_format.set_align('top')
    tittle_format.set_border()

    # Формат первоначальной записи (Для 'Среднее')
    tittle_format_ = workbook.add_format()
    tittle_format_.set_font_script()
    tittle_format_.set_font_size(30)
    tittle_format_.set_bold()
    tittle_format_.set_align('right')
    tittle_format_.set_align('top')
    tittle_format_.set_border()
    tittle_format_.set_bg_color('#E6E6E6')

    # Формат первоначальной записи (2)
    tittle_format_right = workbook.add_format()
    tittle_format_right.set_font_script()
    tittle_format_right.set_font_size(30)
    tittle_format_right.set_bold()
    tittle_format_right.set_align('right')
    tittle_format_right.set_align('top')

    # Формат первоначальной записи (3)
    tittle_format_left = workbook.add_format()
    tittle_format_left.set_font_script()
    tittle_format_left.set_font_size(30)
    tittle_format_left.set_align('left')
    tittle_format_left.set_align('top')

    # Ссылка и город
    worksheet.write(0, 2, f'Данные взяты по данному url: ', tittle_format_right)
    worksheet.write(0, 3, f'    {url}', tittle_format_left)
    worksheet.write(1, 1, f'Город: ', tittle_format_right)

    # Записываем город
    if mode == '1' or mode == 'лента':
        worksheet.write(1, 2, f'  {get_town(get_html(url), mode="лента")}', tittle_format_left)
    elif mode == '2' or mode == 'карта':
        worksheet.write(1, 2, f'  {get_town(get_html_map(url), mode="карта")}', tittle_format_left)

    # Сокращаем дистанцию
    worksheet.set_row(2, 20)

    # Заголовки цен за метр
    worksheet.write(3, 2, f'Цена за метр:              ', tittle_format)
    worksheet.write(3, 1, '', tittle_format)
    worksheet.write(4, 1, f'min: ', tittle_format)
    worksheet.write(5, 1, f'max: ', tittle_format)
    worksheet.write(6, 1, f'Среднее: ', tittle_format_)

    # Значения цен за метр
    worksheet.write(4, 2, f'=MIN(D{chart_start + 2}:D{1000})', workbook.add_format({'align': 'top',
                                                                                    'font_size':
                                                                                        20,
                                                                                    'border': True}))
    worksheet.write(5, 2, f'=MAX(D{chart_start + 2}:D{1000})', workbook.add_format({'align':
                                                                                        'top',
                                                                                    'font_size':
                                                                                        20,
                                                                                    'border': True}))
    worksheet.write(6, 2, f'=AVERAGE(D{chart_start + 2}:D{1000})', workbook.add_format({'align':
                                                                                            'top',
                                                                                        'font_size': 20,
                                                                                        'border': True,
                                                                                        'bg_color': '#E6E6E6'}))

    # Доп.функционал
    worksheet.write(3, 3, 'Площадь, м²:  ', tittle_format)
    worksheet.write(4, 3, 'Стоимость:  ', tittle_format)

    # Рассчеты доп.функционала
    worksheet.write(3, 4, 0, tittle_format_left)
    worksheet.write(4, 4, '=C7*E4', tittle_format_left)

    # Если режим ленты
    if mode == '1' or mode == 'лента':

        # Форматирование исходной ссылки
        base_url = url.split('?')[0]
        page_part = 'p='
        query_part = 'q' + url.split('q')[1] if 'q' in url else ''

        # Определяем колво страниц для web-скребка
        total_pages = get_total_pages(get_html(url))

        # Перебираем каждую страницу
        for i in range(1, user_pages + 1 if user_pages < total_pages else total_pages + 1):
            # Случайная задержка (для надежности)
            time.sleep(1 + (int(random.randrange(1, 1000)) / 1000))

            # Визуализация для пользователя
            print(f'Страница {i}...')

            # Составляем url страницы
            url_gen = base_url + '?' + page_part + str(i) + query_part

            # Обработка страницы и запись данных о ней
            get_data(get_html(url_gen))

    # Если режим "карта"
    elif mode == '2' or mode == 'карта':

        # Форматирование ссылки
        parts = url.split('&')
        page = parts[3][:-1]
        parts.pop(3)

        # Перебираем квартиры
        for i in range(1, 1000000):

            # Конечное форматирование ссылки
            certain_parts = parts.copy()
            certain_parts.insert(3, page + str(i))
            certain_url = '&'.join(certain_parts)

            # Если нужно остановить программу
            if not get_data_map(get_html_map(certain_url)):
                break

    # Ошибка в выборе режима.
    else:
        main.stop = True


# Точка входа
if __name__ == '__main__':

    # Создаем/открываем файл на запись
    workbook = xlsxwriter.Workbook('Avito flats.xlsx')

    # создаем там "лист"
    worksheet = workbook.add_worksheet()

    # Устанавливаем ширину коллон
    worksheet.set_column(2, 2, 22)
    worksheet.set_column(1, 1, 25)
    worksheet.set_column(0, 0, 45)
    worksheet.set_column(4, 4, 150)
    worksheet.set_column(3, 3, 28)

    # Начало таблицы (строка)
    chart_start = 8

    # Устанавливаем высоту первых строчек
    for i in range(chart_start + 1):
        worksheet.set_row(i, 35)

    # формат для заголовка
    head_format = workbook.add_format({'bold': True})
    head_format.set_align('center')
    head_format.set_underline(1)
    head_format.set_font_size(24)
    head_format.set_bg_color('#98FB98')
    head_format.set_locked(True)
    head_format.set_border()

    # Формат для данных
    body_format = workbook.add_format()
    body_format.set_align('center')
    body_format.set_font_size(21)

    # Формат для ссылки
    sink_format = workbook.add_format()
    sink_format.set_align('center')
    sink_format.set_font_size(18)

    # Записываем заголовки
    worksheet.write(chart_start, 0, 'Квартира', head_format)
    worksheet.write(chart_start, 1, 'Стоимость', head_format)
    worksheet.write(chart_start, 2, 'Площадь', head_format)
    worksheet.write(chart_start, 3, 'Цена за метр', head_format)
    worksheet.write(chart_start, 4, 'Ссылка', head_format)

    # Строка в xlxs-файле (используется при записи в xlxs-файл)
    row = chart_start + 1

    # Тело программы
    main()

    # Если введенные параметры корректны.
    if not main.stop:
        # сохраняем и закрываем
        workbook.close()

        print("\n---Writing complete---")
        print('(Данные записаны в файл "Avito flats.xlsx")')

    # Если введенные параметры не корректны.
    else:
        print('---Writing terminated---')
