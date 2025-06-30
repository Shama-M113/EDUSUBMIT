import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(submissions);")
columns = cursor.fetchall()

print("Submissions Table Schema:")
for col in columns:
    print(col)

conn.close()

