from datetime import datetime

def how_much_time(func):
    # Выводит колво затраченного времени на выполнение кода (декоратор)
    def the_all_func(url):
        t1 = datetime.now()  # Запуск замера времени выполнения
        func(url)
        print(f'- Время выполнения: {datetime.now() - t1}')  # Замер времени выполнения

    return the_all_func


def trouble_hunter(func):
    ''' Если происходит ошибка, то возвращаем None '''
    def the_all_funk(address_list):
        try:
            return func(address_list)
        except:
            return None