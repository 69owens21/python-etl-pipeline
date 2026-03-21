import requests
import sqlite3
from bs4 import BeautifulSoup

conn = sqlite3.connect('book_data.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        price REAL
    )
''')

url = 'http://books.toscrape.com/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

books = soup.find_all('article', class_='product_pod')

for book in books:
    title = book.h3.a['title']
    price_text = book.find('p', class_='price_color').text
    # Ensure all non-numeric characters (like currency symbols) are removed before conversion
    price = float(''.join(filter(lambda x: x.isdigit() or x == '.', price_text))) 

    # Corrected line:
    cursor.execute('INSERT INTO books(title, price) VALUES (?,?)', (title, price))

conn.commit()
conn.close()

print("Scraping completed. Data saved to book_data.db")
