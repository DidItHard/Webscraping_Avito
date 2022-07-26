from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from pprint import pprint
from time import sleep
from multiprocessing import Pool
import csv


def find_num_pages(driver):
    global num_pages
    btn = driver.find_elements_by_xpath(
        "//div[@class='pagination-root-2oCjZ']/span[@class='pagination-item-1WyVp']")[-1]
    num_pages = int(btn.text)


def get_links(driver):
    # Находим ссылки на квартиры (на 1 стр)
    flats = driver.find_elements_by_xpath(
        "//div[@class='iva-item-body-NPl6W']/div[@class='iva-item-titleStep-2bjuh']/a")
    return [flat.get_attribute('href') for flat in flats]


def clear_csv(name="flats.csv"):
    with open(name, mode="w"):
        pass


def write_csv(link):
    with open("flats.csv", mode="a", encoding='utf-8', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(link)
        print(link, 'parsed')


def main(url):
    driver = webdriver.Chrome()
    driver.get(url)

    [write_csv((link, ' ')) for link in get_links(driver)]

    driver.close()


if __name__ == '__main__':
    clear_csv()

    # Активируем драйвер (открываем браузер)
    url = 'https://www.avito.ru/yaroslavl/kvartiry/prodam-ASgBAgICAUSSA8YQ'

    # driver = webdriver.Chrome()
    # driver.get(url)

    # Находим кол-во страниц
    # find_num_pages(driver)
    num_pages = 75

    with Pool(15) as p:
        p.map(main, [url + f'?p={i}' for i in range(1, num_pages + 1)])
