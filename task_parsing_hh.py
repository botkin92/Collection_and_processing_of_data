from bs4 import BeautifulSoup
import requests
import json


def get(url, headers, params):
    r = requests.get(
        url=url,
        headers=headers,
        params=params
    )
    return r


def parse(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', class_='vacancy-serp-item')
    comps = []
    for item in items:
        salary_list = get_salary(item.find('div', class_='vacancy-serp-item__sidebar')
                                     .get_text(strip=True))
        comps.append({
            'title': item.find('a', class_='bloko-link').get_text(strip=True),
            'salary_min': salary_list[0],
            'salary_max': salary_list[1],
            'salary_currency': salary_list[2],
            'link': item.find('a', class_='bloko-link').get('href'),
            'site': url.split("/")[2]
        })
    # save(comps)
    return comps


def get_salary(salary_str):
    if not salary_str:
        min_salary = None
        max_salary = None
        currency_salary = None

    elif salary_str.find('от') != -1:
        salary_str = salary_str.replace('\u202f', '').split()
        min_salary = int(salary_str[1])
        max_salary = None
        currency_salary = salary_str[2]

    elif salary_str.find('до') != -1:
        salary_str = salary_str.replace('\u202f', '').split()
        min_salary = None
        max_salary = int(salary_str[1])
        currency_salary = salary_str[2]

    else:
        salary_str = salary_str.replace('\u202f', '').split()
        min_salary = int(salary_str[0])
        max_salary = int(salary_str[2])
        currency_salary = salary_str[3]
    salary_list = [min_salary, max_salary, currency_salary]
    return salary_list


def save(json_data):
    with open('parse_hh.json', 'a', encoding='utf8') as outfile:
        json.dump(json_data, outfile, sort_keys=True, indent=4, ensure_ascii=False)


def pagination(nums_pages=5):
    global url, headers, input_vacancy
    all_data_vacancy = []
    pages = [i for i in range(0, nums_pages)]
    for p in pages:
        params1 = {"page": p,
                   "text": input_vacancy
                   }
        pagi_response = get(url, headers, params1)
        data_vacancy = parse(pagi_response)
        all_data_vacancy.extend(data_vacancy)
    return save(all_data_vacancy)


def pagi_input():
    p = int(input("Введите количество просматриваемых страниц: "))
    if p > 40:
        print('количество страниц не может быть больше 40')
        return pagi_input()
    elif p < 1:
        print('количество страниц не может быть меньше 1')
        return pagi_input()
    else:
        return p


url = 'https://hh.ru/search/vacancy'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/91.0.4472.114 Safari/537.36'}

input_vacancy = input("Введите название вакансии: ")
page1 = pagi_input()  # Запрос кол-ва страниц

info_vacancies = pagination(page1)
