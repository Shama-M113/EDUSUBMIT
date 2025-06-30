import sqlite3

def create_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_usn INTEGER NOT NULL,
            student_name text,
            assignment_id INTEGER NOT NULL,
            submission_filename TEXT NOT NULL,
            submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_name) REFERENCES students(name),
            FOREIGN KEY (student_usn) REFERENCES students (usn),
            FOREIGN KEY (assignment_id) REFERENCES assignments (id)
        )
    ''')
    
    # Commit and close connection
    conn.commit()
    conn.close()
    print("Database setup completed successfully!")

if __name__ == "__main__":
    create_database()
