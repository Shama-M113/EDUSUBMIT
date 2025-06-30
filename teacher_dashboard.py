from flask import render_template, redirect, session, flash
import sqlite3

def get_teacher_dashboard():
    if 'teacher_id' not in session:
        flash("You must log in to access the teacher dashboard.", "error")
        return redirect('/teacher_login')

    teacher_id = session.get('teacher_id')
    teacher_name = session.get('teacher_name', 'Unknown')
    teacher_email = session.get('teacher_email', 'Unknown')

    print("Session Data:", session)

    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, title, description, deadline FROM assignments")
        rows = cursor.fetchall()
        print("Fetched Rows:", rows)

        assignments = [
            {"id": row['id'], "title": row['title'], "description": row['description'], "deadline": row['deadline']}
            for row in rows
        ]

        if not assignments:
            flash("No assignments found. Please create a new assignment to get started.", "info")
    except sqlite3.Error as e:
        print("Database Error:", e)
        flash(f"An error occurred while fetching assignments: {str(e)}", "error")
        assignments = []
    finally:
        conn.close()

    print("Teacher Name:", teacher_name)
    print("Teacher Email:", teacher_email)
    print("Assignments:", assignments)

    return render_template(
        'teacher_dashboard.html',
        teacher_name=teacher_name,
        teacher_email=teacher_email,
        assignments=assignments
    )
