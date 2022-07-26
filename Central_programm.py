import Create_list_Avito
from Flat_page import get_html, get_data
from Parsing_name import parsed_address
from Filling_forms import advanced_search
from Parsing_house import parser_house


def write_csv(data):
    pass


if __name__ == '__main__':
    # Заполняет flats.txt ссылками с авито
    Create_list_Avito.create_list_links_to_flats('https://www.avito.ru/yaroslavskaya_oblast/kvartiry')

    # Находит информацию по всем квартирам [bs4] (нужна многопроцессность)
    archive = []  # Информация о всех квартирах
    with open('flats.txt') as file:
        for url in file.readlines():
            data = get_data(get_html(url.strip()))
            archive.append(data)

    # Перебираем квартиры, находим ссылку и инфу про дом и все записываем [selenium, csv] (нужна многопроцессность)
    for flat_info in archive:
        ''' Находим ссылку на дом и парсим инфу о доме'''
        address = parsed_address(flat_info['Адрес'])
        link_house = advanced_search(list(parsed_address(address).values()))
        house_info = parser_house(link_house)

        all_data = {**flat_info, **house_info}

        # Записываем все в csv
        write_csv(all_data)
