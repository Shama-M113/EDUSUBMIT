import sqlite3
import csv

# Student database
def load_csv_to_db_student(csv_file):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create students table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            usn TEXT NOT NULL UNIQUE,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Read CSV file and insert data into the table
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute('''
                INSERT OR IGNORE INTO students (name, usn, email, password)
                VALUES (?, ?, ?, ?)
            ''', (row['name'], row['usn'], row['email'], row['password']))

    conn.commit()
    conn.close()

# Call the function with your CSV file name for students
load_csv_to_db_student('student.csv')


