from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from time import sleep


def advanced_search(
        address_lst: list = ['Ярославская', 'Ярославль', ('Машиностроителей', 'пр-кт'), '46']):
    class No_data(Exception):
        ''' На сайте нет нужных данных о квартире '''
        pass

    class Not_found(Exception):
        ''' Квартира не найдена '''
        pass

    # Url Расширенного поиска
    url = 'https://www.reformagkh.ru/search/houses-advanced'

    # Запуск сайта
    driver = webdriver.Chrome()
    driver.get(url)
    sleep(0.75)

    # - Регион -
    region = driver.find_element_by_xpath(
        "//input[@name='region']")
    region.send_keys(address_lst[0])
    region.click()
    sleep(0.5)
    region.send_keys(Keys.ARROW_DOWN, Keys.RETURN)
    sleep(4)

    # - Населенный пункт -
    settlement = driver.find_element_by_xpath(
        "//input[@name='settlement']")
    settlement.send_keys(address_lst[1])
    settlement.click()
    sleep(0.5)
    settlement.send_keys(Keys.ARROW_DOWN, Keys.RETURN)
    sleep(1)

    # - Улица -
    street = driver.find_element_by_xpath(
        "//input[@name='street']")
    street.send_keys(address_lst[2][0])
    tag = address_lst[2][1]  # Тег из адреса (мол это улица или периулок и тп
    street.click()
    sleep(0.5)

    streets = driver.find_elements_by_xpath("//ul[4]/li")  # Доступные улицы
    # Вычленяем названия доступных улиц
    street_names = [(street_name.find_element_by_tag_name('div').text, i) for i, street_name in
                    enumerate(streets)]
    # Находим доступные улицы с нашим тегом
    good_street_names = list(filter(lambda couple: '(' + tag + ')' in couple[0], street_names))

    # Если есть совпадения тега и доступных улиц
    if good_street_names:
        # Нужная улица
        good_street_name = good_street_names[-1]
        # Индекс нужной улицы
        good_street_name_index = good_street_name[1]
        # Кликаем на нужную улицу
        streets[good_street_name_index].click()
    else:
        # Выбираем первую улицу
        streets[0].click()

    # street.send_keys(Keys.ARROW_DOWN, Keys.RETURN)
    sleep(0.5)

    # - Номер дома -
    house = driver.find_element_by_xpath(
        "//input[@name='house']")
    house.send_keys(address_lst[3])
    house.click()
    sleep(0.5)
    house.send_keys(Keys.ARROW_DOWN, Keys.RETURN)
    sleep(1)

    # Находим кнопку "Найти"
    btn_find = driver.find_element_by_xpath(
        "//button[@class='px-5 py-3 br-8 btn btn-primary text-uppercase f-18 lh-20']")
    btn_find.click()
    sleep(1)

    # Результат поиска
    result_link = False
    lines_of_links = driver.find_elements_by_xpath(
        "//div[@class='container ']/table/tbody/tr")

    # Перебираем выпавшие ссылки, находим нужную
    for line_of_link in lines_of_links:
        parts = line_of_link.find_elements_by_tag_name('td')
        section_of_site, almost_link = parts[1], parts[0]

        # Если раздел сайта у ссылки это 'Жилищный фонд', то успех
        if section_of_site.text == 'Жилищный фонд' or section_of_site.text == 'Мой дом':
            result_link = almost_link.find_element_by_tag_name('a').get_attribute('href')
            driver.close()
            return result_link

    # Если не нашлась ссылка(
    if not result_link:
        driver.close()
        return (Not_found('--- Квартира не найдена ---'))

    driver.close()


if __name__ == '__main__':
    # Проверка имени
    try:
        address_list = list({'Регион': 'Адыгея', 'Город': 'Адыгея', 'Улица': ('Бжегокайская', 'ул'),
                             'Номер дома': '90/1к2'}.values())
        assert None not in address_list

        # Проверка самого взаимодействия с формами
        try:
            print(advanced_search(address_lst=address_list))
        except Exception as E:
            print(f'Что за криворукий все это написал?! \n{E}')

    except AssertionError:
        print('Плохое имя')