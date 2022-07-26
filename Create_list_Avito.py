''' Создает файл flats.txt с ссылками на объявления с квартирами на Avito'''



from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random
from time import sleep



def create_list_links_to_flats(url='https://www.avito.ru/yaroslavskaya_oblast/kvartiry', pages: int = -1):
    ''' Создает список ссылок на квартиры в Avito '''

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

        pages = soup.find('div', class_='pagination-root-2oCjZ')
        total_pages = pages.find_all('span')[-2].text

        return int(total_pages)

    def get_links_page(html):
        ''' Работает с одной страницей. Берет из нее данные по всем квартирам и
        записывает их в xlxs-файл '''

        soup = BeautifulSoup(html, 'lxml')

        # Находим все квартиры
        # flats = soup.find_all('div',
        #                       class_='iva-item-root-G3n7v photo-slider-slider-15LoY iva-item-list-2_PpT iva-item-redesign-1OBTh items-item-1Hoqq items-listItem-11orH items-redesignItem-1EDEr js-catalog-item-enum')
        # Перебираем квартиры
        # for flat in flats:
        links = ['https://www.avito.ru' + i.get('href') for i in soup.find_all('a',
                                                                               class_='link-link-39EVK link-design-default-2sPEv title-root-395AQ iva-item-title-1Rmmj title-listRedesign-3RaU2 title-root_maxHeight-3obWc')]

        return links

    def clean_txt(name="flats.txt"):
        with open(name, mode="w", encoding='utf-8', newline='') as file:
            pass

    def main_for_process(url, name="flats.txt"):
        ''' Находит и записывает ссылки '''

        # Рандомная задержка для ухода от блокировок
        sleep(round(random.uniform(0.25, 1.5), 2))

        links = get_links_page(get_html(url))
        links = [str(link) + '\n' for link in links]

        with open(name, mode="a", encoding='utf-8', newline='') as file:
            file.writelines(links)
            print('page have written')


    clean_txt() # Очищает flats.txt
    total_pages = get_total_pages(get_html(url)) # Доступные страницы в источнике (Avito)

    # Соблюдаем ограничение на страницы
    if pages >= 0 and pages <= total_pages: # Если нужно меньше, чем есть, то берем, скольно нужно.
        needed_pages = pages
    else: # Если нужно больше, чем все страницы, то просто берем все доступные страницы.
        needed_pages = total_pages  # Нужное количество страниц для парсинга

    quantity_processes = 15 if needed_pages >= 15 else needed_pages # Определем кол-во потоков (не больше 15)
    assert quantity_processes <= 15 # Проверка (не должно быть больше 15)

    # Запускаем многопоточно парсинг
    with Pool(15) as p:
        p.map(main_for_process, [url + f'?p={i}' for i in range(1, needed_pages + 1)])


if __name__ == '__main__':
    ''' Создаем список ссылок на квартиры в Avito '''
    create_list_links_to_flats(url='https://www.avito.ru/yaroslavskaya_oblast/kvartiry/prodam-ASgBAgICAUSSA8YQ', pages=3)
