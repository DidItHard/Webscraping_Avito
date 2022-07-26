import requests
from multiprocessing import Pool
from requests.auth import HTTPProxyAuth

proxyDict = {
    'http': '217.29.62.214:13095',
    'https': '217.29.62.214:13095'
}
auth = HTTPProxyAuth('0X6fLs', 'yrjaoL')

# Тестируем купленный прокси
try:
    r = requests.get("http://www.google.com", proxies=proxyDict, auth=auth)
    print('It is alive!')
except Exception as E:
    print('It is dead: ' + E.__class__.__name__)
    print(E)



def check_proxy(px):
    try:
        proxyDict = {
            'http': px,
            'https': px
        }
        # px = ':'.join(['200.89.178.159', '8000'])
        requests.get("https://www.google.com/", proxies=proxyDict, timeout=3)
        print('--' + px + ' is alive')
    except Exception as x:
        print('--' + px + ' is dead: ' + x.__class__.__name__)
        print(x)
        # print(x)
        return False
    return True
