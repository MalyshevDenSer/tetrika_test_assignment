'''
Задача №2.
В нашей школе мы не можем разглашать персональные данные пользователей,
но чтобы преподаватель и ученик смогли объяснить нашей поддержке, кого они
имеют в виду (у преподавателей, например, часто учится несколько Саш), мы
генерируем пользователям уникальные и легко произносимые имена. Имя у нас
состоит из прилагательного, имени животного и двузначной цифры. В итоге
получается, например, "Перламутровый лосось 77". Для генерации таких имен
мы и решали следующую задачу:
Получить с русской википедии список всех животных (https://inlnk.ru/jElywR)
и вывести количество животных на каждую букву алфавита.
Результат должен получиться в следующем виде:
А: 642
Б: 412
В:....


Счел ненужным выводить имена на латинице.
'''


from typing import Union
from bs4 import BeautifulSoup, ResultSet
import requests


HOST = 'https://ru.wikipedia.org'
FIRST_PAGE = BeautifulSoup(requests.get \
    (f'{HOST}/wiki/Категория:Животные по алфавиту').content, 'lxml')
LATIN_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def main(page: BeautifulSoup) -> None:
    '''
    Создание и обновление словаря, нахождение строк с имена животных,
    перемещение на следующую страницу и вызов результата программы
    '''
    animal_number_dict = {}
    print('Перехожу на первую страницу списка имен животных')
    while True:
        html_names = page.find(class_= 'mw-category mw-category-columns'). \
            find_all({'a': "title"}) # нахождение строк с именами в html файле
        animal_number_dict = add_animal_to_dict(html_names, animal_number_dict)
        page = find_next_page(page)
        if page is None: # проверка закончился ли список имен
            print_result(animal_number_dict)
            break


def add_animal_to_dict(html_names: ResultSet, animal_number_dict: dict) -> dict:
    '''
    Считываем имена всех животных на странице, прибавляем значение в словаре
    по первой букве животного, возвращаем обновленный или необновленный словарь

    Если нам встречается имя животного начинающегося с латинской буквы, не
    включаем его в словарь(несколько латинских имен животных встречается среди
    русских имен животных)
    '''
    for html_name in html_names:
        animal_name = html_name.get('title')
        print('Обрабатываю имя животного: ' + animal_name)
        if animal_name[0] in LATIN_LETTERS:
            return animal_number_dict
        if animal_name[0] in animal_number_dict:
            animal_number_dict[animal_name[0]] += 1
        else:
            animal_number_dict[animal_name[0]] = 1
    print(animal_number_dict)
    return animal_number_dict


def find_next_page(current_page: BeautifulSoup) -> Union[None, BeautifulSoup]:
    '''
    Проверяем буквенные указатели на странице, если они состоят из русских
    букв - передаем следующую страницу, если нет - возвращаем None (это будет
    означать что алгоритм прошагал весь русский алфваит).
    '''
    for letter_index in current_page.find( \
            class_='mw-category mw-category-columns').find_all("h3"):
        print('На этой странице встречался буквенный указатель: ' + letter_index.text)
        if letter_index.text in LATIN_LETTERS:
            print('На этой странице найден буквенный указатель с латинской буквой')
            return None
    print('Перехожу к следующей странице:')
    next_page_href = current_page.find(string='Следующая страница', \
        title="Категория:Животные по алфавиту").get('href')
    next_page = BeautifulSoup(requests.get(HOST + next_page_href).content, 'lxml')
    return next_page


def print_result(dict_to_print: dict) -> None:
    '''
    Выводим финальный словарь построчно
    '''
    print('\n\n\nРЕЗУЛЬТАТ:\n\n\n')
    for letter_number in sorted(dict_to_print.items()):
        print(letter_number[0] + ': ' + str(letter_number[1]))


main(FIRST_PAGE)
