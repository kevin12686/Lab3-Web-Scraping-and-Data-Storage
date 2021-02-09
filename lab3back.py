import json
import sqlite3
import re
import os
import requests
from bs4 import BeautifulSoup

TARGET_URL = 'https://www.payscale.com/college-salary-report/best-schools-by-state/2-year-colleges/california/page/%d'
TOTAL_PAGES = 2


def create_db(data_list):
    if os.path.exists('data.db'):
        os.remove('data.db')
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE colleges (
    name varchar(255) PRIMARY KEY,
    url varchar(255),
    sector varchar(255),
    starting_salary int unsigned,
    mid_career_salary int unsigned,
    STEM_degrees int unsigned);
    ''')
    conn.commit()
    colleges = [tuple(data.values()) for data in data_list]
    cursor.executemany('INSERT INTO colleges VALUES (?, ?, ?, ?, ?, ?);', colleges)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    data_list = list()
    for p in range(1, TOTAL_PAGES + 1):
        url = TARGET_URL % p
        content = requests.get(url).text
        soup = BeautifulSoup(content, 'html.parser')
        rows = soup.find_all('tr', class_='data-table__row')
        for row in rows:
            data = dict()
            try:
                data['name'] = row.find(class_='csr-col--school-name').span.next_sibling.a.text
                data['url'] = 'https://www.payscale.com%s' % row.find(class_='csr-col--school-name').span.next_sibling.a.get('href')
            except AttributeError:
                data['name'] = row.find(class_='csr-col--school-name').span.next_sibling.text
                data['url'] = None
            data['sector'] = row.find(class_='csr-col--school-type').span.next_sibling.text
            cursor = row.find(class_='csr-col--right')
            data['starting_salary'] = int(re.sub('\D', '', cursor.span.next_sibling.text))
            cursor = cursor.next_sibling
            data['mid_career_salary'] = int(re.sub('\D', '', cursor.span.next_sibling.text))
            cursor = cursor.next_sibling.next_sibling
            data['STEM_degrees'] = int(re.sub('\D', '', cursor.span.next_sibling.text))
            data_list.append(data)
    with open('data.json', 'w') as f:
        json.dump(data_list, f, indent=4)

    with open('data.json', 'r') as f:
        create_db(json.load(f))
