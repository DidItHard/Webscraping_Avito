import datetime
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from time import sleep


def parser_house(url: str):
    ''' Парсит данные о квартире на готовой страничке "Реформы ЖКХ"'''

    def random_delay(t1=0.4, t2=1.5):
        import random
        # Случайная задержка
        sleep(round(random.uniform(t1, t2), 2))

    def add_lines_to_dict(lines):
        ''' Переносит информацию из строк в словарь '''
        for line in lines:
            # Элементы строки
            parts = [part.text for part in line.find_elements_by_tag_name('td') if part.text]

            # Если строка нам подходит
            if len(parts) == 2:
                name, value = parts
                dictionary_lines[name] = value

    def dictionary_selection(dictionary_lines):
        ''' # Убирает лишнее и уточняет невошедшее '''
        output_dictionary = dict()

        needed_lines = ['Год постройки', 'Год ввода дома в эксплуатацию',
                        'Серия, тип постройки здания', 'Тип дома', 'Дом признан аварийным',
                        'наибольшее, ед', 'наименьшее, ед', 'Количество подъездов, ед',
                        'Количество лифтов, ед', 'общее, ед', 'жилых, ед', 'нежилых, ед',
                        'Кадастровый номер', 'Тип перекрытий', 'Материал несущих стен']

        # Перебираем все нужные нам характеристики квартиры
        for spec in needed_lines:
            # if spec in dictionary_lines.keys():
            output_dictionary[spec] = '-'
            for key in dictionary_lines.keys():
                if spec.lower() in key.lower():  # Если нашли нужные нам строчки
                    output_dictionary[spec] = dictionary_lines[key]
                    break

        return output_dictionary

    # Активируем драйвер (открываем браузер)
    driver = webdriver.Chrome()
    driver.get(url)

    # Кнопка "Паспорт"
    btn_pasport = driver.find_element_by_xpath(
        "//div[@class='container d-flex justify-content-center']/a")
    btn_pasport.click()  # Нажимаем
    random_delay(0.5, 1)

    dictionary_lines = dict()  # Словарь всей инфы

    # Находим все строки на странице "Общие сведения"
    lines = driver.find_elements_by_xpath("//table[@class='w-100 simple-table']/tbody/tr")

    # Заносим строки со страницы "Общие сведения" в словарь
    add_lines_to_dict(lines)

    # Переходим в "Конструктивные элементы дома"
    btn_constructive_elems = driver.find_element_by_xpath(
        "//div[@id='headingTwo']/a")
    btn_constructive_elems.click()
    random_delay(0.5, 1)

    # Заносим строки со страницы "Конструктивные элементы дома" в словарь
    lines = driver.find_elements_by_xpath(
        "//div[@class='tab-content fade tab-pane active show']/table[@class='w-100 simple-table']/tbody/tr")
    add_lines_to_dict(lines)

    # Теперь вся полезная инфа в dictionary_lines

    # Обработали наш словарь
    dictionary_lines = dictionary_selection(dictionary_lines)

    # Закрываем браузер
    driver.quit()

    return dictionary_lines


if __name__ == '__main__':
    print(parser_house('https://www.reformagkh.ru/myhouse/profile/view/9012239'))
