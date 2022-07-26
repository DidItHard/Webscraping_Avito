from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def trouble_hunter(func):
    ''' Если происходит ошибка, то возвращаем None '''

    def the_all_funk(address_list):
        try:
            return func(address_list)
        except:
            return None

    return the_all_funk


def how_much_time(func):
    # Выводит колво затраченного времени на выполнение кода (декоратор)
    def the_all_func(address_list: list):
        t1 = datetime.now()  # Запуск замера времени выполнения
        func(address_list)
        print(f'- Время выполнения: {datetime.now() - t1}')  # Замер времени выполнения

    return the_all_func


@how_much_time
@trouble_hunter
def advanced_search(
        address_list: list = ['Ярославская', 'Ярославль', ('Машиностроителей', 'пр-кт'), '46']):
    class No_data(Exception):
        ''' На сайте нет нужных данных о квартире '''
        pass

    class Not_found(Exception):
        ''' Квартира не найдена '''
        pass

    def fill_region(driver):
        # - Регион -
        region = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, "//input[@name='region']")))
        region.send_keys(address_list[0])
        region.click()
        WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, "//ul[@id='ui-id-1']/li"))).click()

    def fill_district(driver):
        # - Район -
        if len(address_list) == 5:
            district_str = address_list[1]
            district = WebDriverWait(driver, 10).until(
                ec.element_to_be_clickable((By.XPATH, "//input[@name='district']")))
            district.send_keys(district_str)
            district.click()
            print('(Я тут)')
            # WebDriverWait(driver, 10).until(
            #     ec.element_to_be_clickable((By.XPATH, "//ul[@id='ui-id-90']/li"))).click()
            district.send_keys(Keys.ARROW_DOWN, Keys.RETURN)  # Вроде костыль

            address_list.pop(1)  # Удаляем, чтобы остальная часть программы работала, как раньше
            print(len(address_list))

    def fill_settlement(driver):
        # - Населенный пункт -
        settlement = WebDriverWait(driver, 20).until(
            ec.element_to_be_clickable((By.XPATH, "//input[@name='settlement']")))
        settlement.send_keys(address_list[1])
        settlement.click()
        WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, "//ul[3]/li"))).click()

    def new_fill_settlement(driver):
        def select_the_settlements(driver):
            ''' Сложная функция по выбору правильного населенного пункта '''

            # Доступные улицы
            settlements = WebDriverWait(driver, 10).until(
                ec.visibility_of_all_elements_located((By.XPATH, "//ul[3]/li")))
            # streets = driver.find_elements_by_xpath("//ul[4]/li")

            # Вычленяем названия доступных населенных пунктов
            settlements_names = [(settlements_name.find_element_by_tag_name('div').text, i) for
                                 i, settlements_name
                                 in
                                 enumerate(settlements)]
            # Находим доступные н.с. с нашим тегом
            good_settlement_names = list(
                filter(lambda couple: '(' + tag + ')' in couple[0], settlements_names))

            # Если есть совпадения тега и доступных н.с.
            if good_settlement_names:
                # Нужная улица
                good_settlement_name = good_settlement_names[-1]
                # Индекс нужной улицы
                good_settlement_name_index = good_settlement_name[1]
                # Кликаем на нужную улицу
                settlements[good_settlement_name_index].click()
            else:
                # Выбираем первую улицу
                settlements[0].click()

        settlements = WebDriverWait(driver, 20).until(
            ec.element_to_be_clickable((By.XPATH, "//input[@name='street']")))
        settlements.send_keys(address_list[2][0])
        # Тег из адреса (мол это улица или периулок и тп)
        tag = address_list[2][1]
        settlements.click()
        select_the_settlements(driver)

    def fill_street(driver):
        ''' - Улица - '''

        def select_the_street(driver):
            ''' Сложная функция по выбору правильной улицы '''

            # Доступные улицы
            streets = WebDriverWait(driver, 10).until(
                ec.visibility_of_all_elements_located((By.XPATH, "//ul[4]/li")))
            # streets = driver.find_elements_by_xpath("//ul[4]/li")

            # Вычленяем названия доступных улиц
            street_names = [(street_name.find_element_by_tag_name('div').text, i) for i, street_name
                            in
                            enumerate(streets)]
            # Находим доступные улицы с нашим тегом
            good_street_names = list(
                filter(lambda couple: '(' + tag + ')' in couple[0], street_names))

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

        street = WebDriverWait(driver, 20).until(
            ec.element_to_be_clickable((By.XPATH, "//input[@name='street']")))
        street.send_keys(address_list[2][0])
        # Тег из адреса (мол это улица или периулок и тп)
        tag = address_list[2][1]
        street.click()
        select_the_street(driver)

    def fill_house(driver):
        # - Номер дома -
        house = WebDriverWait(driver, 20).until(
            ec.element_to_be_clickable((By.XPATH, "//input[@name='house']")))
        # house = driver.find_element_by_xpath((By.XPATH, "//input[@name='house']")) # Костыль
        house.send_keys(address_list[3])
        house.click()

        try:  # Ждем появления шторки с вариантами
            driver.find_element_by_xpath("//ul[@id='ui-id-186']")
            house.send_keys(Keys.ARROW_DOWN, Keys.RETURN)  # Жмем "Вниз" и Enter для выбора варианта
        except:  # Если она не появилась, то Enter не жмем
            pass

    def push_the_FindButton(driver):
        ''' Находит и нажимиет кнопку "Найти" '''
        btn_find = driver.find_element_by_xpath(
            "//form[@class='my-3 pt-1']/div[@class='form ajax-address']/button")
        btn_find.click()

    def get_link_tech(driver):
        ''' Работает уже на странице со ссылками'''
        # Результат поиска
        result_link = False
        WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located(
                (By.XPATH, "//div[@class='container ']/table")))

        lines_of_links = WebDriverWait(driver, 10).until(
            ec.visibility_of_all_elements_located(
                (By.XPATH, "//div[@class='container ']/table/tbody/tr")))
        # lines_of_links = driver.find_elements_by_xpath(
        #     "//div[@class='container ']/table/tbody/tr")

        # Перебираем выпавшие ссылки, находим нужную
        for line_of_link in lines_of_links:
            parts = line_of_link.find_elements_by_tag_name('td')
            section_of_site, almost_link = parts[1], parts[0]

            # Если раздел сайта у ссылки это 'Жилищный фонд' или 'Мой дом', то успех
            if section_of_site.text == 'Жилищный фонд' or section_of_site.text == 'Мой дом':
                result_link = almost_link.find_element_by_tag_name('a').get_attribute('href')
                driver.close()
                return result_link

        # Если не нашлась ссылка(
        if not result_link:
            driver.close()
            return (Not_found('--- Квартира не найдена ---'))

        driver.close()

    def get_link_primary(driver):
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

    def random_delay(t1=0.4, t2=1.5):
        import random
        # Случайная задержка
        sleep(round(random.uniform(t1, t2), 2))

    # Url Расширенного поиска
    url = 'https://www.reformagkh.ru/search/houses-advanced'
    driver = webdriver.Chrome()
    driver.get(url)

    # Заполняем графу "регион"
    fill_region(driver)
    random_delay()

    # Заполняем графу "район" (если он подается во входных данных)
    fill_district(driver)
    random_delay()

    # Заполняем графу "населенный пункт"
    fill_settlement(driver)
    random_delay()

    # Заполняем графу "улица"
    fill_street(driver)
    random_delay()

    # Заполняем графу "дом"
    fill_house(driver)
    random_delay(1, 1.2)

    # Нажимаем кнопку "Найти"
    push_the_FindButton(driver)
    random_delay(1, 2)

    # Находим нужную ссылку
    THE_link = get_link_tech(driver)

    return THE_link


if __name__ == '__main__':
    address_list = ['Ярославская', 'Ростовский', 'Ново-Никольское', ('Совхозная', 'ул'), '5']
    print(advanced_search(address_list=address_list))
