import csv
import random
import xml.etree.ElementTree as ET
from pathlib import Path

FOLDER = Path(__file__).resolve().parent


def read_books(filename, encoding):
    with (FOLDER / filename).open('r', encoding=encoding, newline='') as file:
        return list(csv.DictReader(file, delimiter=';'))


def parse_price(value):
    try:
        return float(value.strip().replace(',', '.').replace(' ', ''))
    except (ValueError, AttributeError):
        return None


def find_books(books, query):
    return [book for book in books
            if query.lower() in book['Book-Author'].lower()
            and (price := parse_price(book['Price'])) is not None
            and price <= 200]


def main():
    # Для задания выбран books-en.csv: здесь есть год издания.
    books = read_books('books-en.csv', 'cp1251')
    russian_books = read_books('books.csv', 'cp1251')

    print('Лабораторная работа №2. Вариант 4')
    print('Количество названий длиннее 30 символов (books-en.csv):',
          sum(len(book['Book-Title']) > 30 for book in books))
    print('Количество названий длиннее 30 символов (books.csv):',
          sum(len(book['Название']) > 30 for book in russian_books))

    # Поиск автора. Для варианта 4 цена не должна превышать 200 рублей.
    author = input('Введите имя автора для поиска: ').strip()
    if author:
        matches = find_books(books, author)
        print('Найдено книг стоимостью до 200 рублей:', len(matches))
        for book in matches[:30]:
            print(f"{book['Book-Author']}. {book['Book-Title']} — {book['Price']} руб.")
        if len(matches) > 30:
            print('Показаны первые 30 книг.')
    else:
        print('Поиск пропущен.')

    # Генератор библиографических ссылок: 20 разных записей.
    available = [b for b in books if b['Book-Author'] and b['Book-Title']
                 and b['Year-Of-Publication']]
    random.seed(4)
    selection = random.sample(available, 20)
    with (FOLDER / 'bibliography_variant4.txt').open('w', encoding='utf-8') as output:
        for number, book in enumerate(selection, start=1):
            output.write(f"{number}. {book['Book-Author']}. {book['Book-Title']} - "
                         f"{book['Year-Of-Publication']}\n")
    print('Файл bibliography_variant4.txt сохранён.')

    # XML: словарь NumCode — CharCode. Коды остаются строками, чтобы сохранить нули.
    root = ET.parse(FOLDER / 'currency.xml').getroot()
    currencies = {}
    for valute in root.findall('Valute'):
        num = valute.findtext('NumCode')
        char = valute.findtext('CharCode')
        if num and char:
            currencies[num] = char
    print('Словарь валют (NumCode — CharCode):', currencies)

    # Дополнительное задание: издательства без повторений.
    publishers = sorted({b['Publisher'].strip() for b in books if b['Publisher'].strip()})
    (FOLDER / 'publishers_variant4.txt').write_text('\n'.join(publishers) + '\n', encoding='utf-8')
    print('Количество уникальных издательств:', len(publishers))
    print('Список сохранён в publishers_variant4.txt')

    # Дополнительное задание: популярность по количеству скачиваний.
    popular = sorted(books, key=lambda b: int(b['Downloads']) if b['Downloads'].isdigit() else 0,
                     reverse=True)[:20]
    with (FOLDER / 'top20_variant4.txt').open('w', encoding='utf-8') as output:
        for number, book in enumerate(popular, start=1):
            line = (f"{number}. {book['Book-Title']} — {book['Book-Author']} "
                    f"(скачиваний: {book['Downloads']})")
            print(line)
            output.write(line + '\n')
    print('Рейтинг сохранён в top20_variant4.txt')


if __name__ == '__main__':
    main()
