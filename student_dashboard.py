from flask import render_template, redirect, session
import sqlite3

def get_student_dashboard():
    # Ensure the student is logged in
    if 'student_id' not in session:
        return redirect('/student_login')  # Redirect to login if not logged in

    # Fetch student details from session
    student_name = session['student_name']
    student_usn = session['student_usn']
    student_email = session['student_email']

    # Connect to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Fetch assignments from the database
    cursor.execute("SELECT id, title, description, deadline FROM assignments")
    rows = cursor.fetchall()

    conn.close()

    # Prepare the list of assignments with the submission status
    assignments = [
        {"id": row[0], "title": row[1], "description": row[2], "deadline": row[3]}
        for row in rows
    ]

    # Return the rendered dashboard page with the assignments
    return render_template('student_dashboard.html', 
                           name=student_name, 
                           usn=student_usn, 
                           email=student_email,
                           assignments=assignments)