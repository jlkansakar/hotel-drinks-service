import sqlite3
import csv

def initialize_db():
    conn = sqlite3.connect('drinks.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS drinks (
            drink_id INTEGER PRIMARY KEY AUTOINCREMENT,
            drink_name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            sale_count INT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database and table 'drinks' initialized successfully.")


def populate_db():
    conn = sqlite3.connect('drinks.db')
    cursor = conn.cursor()

    with open("drinks_menu_with_sales.csv", mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file, delimiter=',')
        for row in csv_reader:
            cursor.execute('''
                INSERT INTO drinks (drink_name, category, price, sale_count)
                VALUES (?, ?, ?, ?)
            ''', (row['Drink Name'], row['Category'], row['Price (DKK)'], row['Units Sold']))

    conn.commit()
    conn.close()
    print("Database populated successfully from CSV file.")


if __name__ == "__main__":
    initialize_db()
    populate_db()