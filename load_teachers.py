import sqlite3
import csv

# Student database
def load_csv_to_db_teacher(csv_file):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS teachers")

    # Create students table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            teacher_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Read CSV file and insert data into the table
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute('''
                INSERT OR IGNORE INTO teachers (teacher_id, name, email, password)
                VALUES (?, ?, ?, ?)
            ''', (row['teacher_id'],row['name'],  row['email'], row['password']))

    conn.commit()
    conn.close()

# Call the function with your CSV file name for students
load_csv_to_db_teacher('teachers.csv')


