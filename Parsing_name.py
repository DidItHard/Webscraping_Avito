from pprint import pprint


def parsed_address(address: str = 'Ярославская область, Ярославль, ул. Терешковой, 15/8',
                   link=None):
    parts_dictionary = {'Регион': '-', 'Район': '-', 'Город': '-', 'Улица': '-', 'Номер дома': '-'}

    street_index, region_index = None, None

    def find_district(address):
        ''' Вырезает район '''
        nonlocal street_index

        # Чтобы отслеживаеть ошибки и наладить процесс
        try:
            parts = address.split(', ')

            # Находим эти теги в адресе, чтобы найти улицу (и т.п.)
            tags = ['р-н', 'округ']

            # Перебираем все части адреса
            for i, part in enumerate(parts):
                # Если уже нашли улицу и т.п.
                if parts_dictionary['Район'] != '-':
                    break

                # Перебираем теги в адресе
                for tag in tags:
                    if tag in part:
                        result_part = part

                        # Вычлиняем именно результат
                        result = ' '.join([i for i in result_part.split(' ') if i != tag])
                        # Убираем точки из тега
                        tag = tag.replace('.', '')
                        # Записываем
                        parts_dictionary['Район'] = result
                        # parts_dictionary['Район'] = (result, tag)
                        break


        # Если выпала какая-то ошибка
        except:
            parts_dictionary['Район'] = '-Error-'

        # Если "Райна" нет в адресе
        if parts_dictionary['Район'] == '-':
            parts_dictionary.pop('Район')

    def find_street(address):
        ''' Вырезает улицу '''
        nonlocal street_index

        # Чтобы отслеживаеть ошибки и наладить процесс
        try:
            parts = address.split(', ')

            # Находим эти теги в адресе, чтобы найти улицу (и т.п.)
            tags = ['ул.', 'пр.', 'пр-д', 'пр-т', 'ш.', 'пер.']

            # Перебираем все части адреса
            for i, part in enumerate(parts):
                # Если уже нашли улицу и т.п.
                if parts_dictionary['Улица'] != '-':
                    break

                # Перебираем теги в адресе
                for tag in tags:
                    if tag in part:
                        result_part = part
                        street_index = i

                        # Вычлиняем именно результат
                        result = ' '.join([i for i in result_part.split(' ') if i != tag])
                        # Убираем точки из тега
                        tag = tag.replace('.', '')
                        # Записываем
                        parts_dictionary['Улица'] = (result, tag)
                        break

            # Если улица не нашлась
            if parts_dictionary['Улица'] == '-':
                parts_dictionary['Улица'] = None

        # Если выпала какая-то ошибка
        except:
            parts_dictionary['Улица'] = '-Error-'

    def find_house(address):
        ''' Находит номер дома '''
        nonlocal street_index

        # Чтобы отслеживаеть ошибки и наладить процесс
        try:
            # Если нашлась улица
            if isinstance(street_index, int):
                parts_dictionary['Номер дома'] = address.split(', ')[street_index + 1]
            else:
                parts_dictionary['Номер дома'] = None

        # Если выпала какая-то ошибка
        except:
            parts_dictionary['Номер дома'] = '-Error-'

    def find_region(address):
        nonlocal region_index

        # Чтобы отслеживаеть ошибки и наладить процесс
        try:

            parts = address.split(', ')
            tags = ['область', 'Республика', 'край']

            # Перебираем все части адреса
            for i, part in enumerate(parts):
                # Перебираем теги в адресе
                for tag in tags:
                    if tag in part:
                        result_part = part
                        region_index = i

                        # parts_dictionary['Улица'] = result_part.split(' ')[-1]
                        result = ' '.join([i for i in result_part.split(' ') if i != tag])
                        parts_dictionary['Регион'] = result

            # Если улица не нашлась
            if parts_dictionary['Регион'] == '-':
                parts_dictionary['Регион'] = None

        # Если выпала какая-то ошибка
        except Exception as E:
            parts_dictionary['Регион'] = '-Error-'

    def find_town(address):
        ''' Находит город '''
        nonlocal region_index

        # Чтобы отслеживаеть ошибки и наладить процесс
        try:

            # Если нашли регион
            if isinstance(region_index, int):
                expected_town = address.split(', ')[region_index + 1]

                tags = ['р-н', 'округ']

                # Проверяем, чтобы город не был негородом
                for tag in tags:
                    if tag in expected_town:
                        expected_town = address.split(', ')[region_index + 2]

                # Город должен быть одним словом
                if ' ' in expected_town:
                    expected_town = expected_town.split(' ')[-1]

                # Записываем в словарь
                parts_dictionary['Город'] = expected_town

            # Если не нашли регион (ищем регион и город)
            elif isinstance(link, str):
                from geopy.geocoders import Nominatim
                from fake_useragent import UserAgent

                def find_town_region(url):
                    ''' Находит регион и название города по его латинскому написанию,
                     взятомого из ссылки '''

                    def advanced_find_region(location):
                        '''Определяем регион'''
                        parts = location.split(', ')

                        tags = ['область', 'край', 'Республика']
                        region = ''

                        # Пытаемся найти слова "область", "республика" и "край"
                        for part in parts:
                            # Если регион уже найден
                            if region:
                                break

                            for tag in tags:
                                if tag in part:
                                    region = [i for i in part.split(' ') if i != tag][0]
                                    break

                        # Если не нашли ключевые слова
                        if not region:
                            # Убираем Россию с конца
                            local_parts = parts[:-1]

                            # Убираем все части, где есть цифры
                            nums = [str(i) for i in range(10)]
                            for i, part in enumerate(parts):
                                for num in nums:
                                    if num in part:
                                        local_parts.ksdjhfgjk(i)

                            # Находим часть в одно слово
                            for part in reversed(local_parts):
                                if len(part.split()) == 1:
                                    region = part
                                    break

                        if not region:
                            return None
                        else:
                            return region

                    latin_town = url.split('/')[3].strip()

                    ua = UserAgent()

                    geolocator = Nominatim(user_agent=str(ua.random))
                    location = str(geolocator.geocode(latin_town).address)

                    parts = location.split(', ')

                    # Определяем город
                    town = parts[0]
                    # Город должен быть одним словом
                    if ' ' in town:
                        town = town.split(' ')[-1]

                    # Определяем регион
                    # region = parts[2].split(' ')[0]
                    region = advanced_find_region(location)

                    return (town, region)

                town, region = find_town_region(url=link)

                parts_dictionary['Город'] = town
                parts_dictionary['Регион'] = region


        # Если выпала какая-то ошибка
        except:
            parts_dictionary['Город'] = '-Error-'

    try:
        find_region(address)
        find_town(address)
        find_street(address)
        find_house(address)
        find_district(address)

        return parts_dictionary
    except Exception as E:
        return ('"parsed_address": ', E)


if __name__ == '__main__':
    print(list(
        parsed_address('ул. Московская, д. 118, корп. 2',
                       'https://www.avito.ru/krasnodar/kvartiry/2-k._kvartira_524m_716et._2114886462').values()))

    print(list(
        parsed_address('Ярославская область, Ростовский р-н, с. Ново-Никольское, Совхозная ул., 5',
                       'https://www.avito.ru/semibratovo/kvartiry/2-k._kvartira_50m_13et._1281950308').values()))

    # with open('addresses_links.txt', encoding='utf-8') as file:
    #     for line in file.readlines():
    #         try:
    #             address, link = line.strip().split('; ')
    #             print(parsed_address(address, link))
    #         except ValueError:
    #             print(line.strip())
    #         except Exception as E:
    #             print(E)
    # pprint(list(map(parsed_address, [line.strip() for line in file.readlines()])))
