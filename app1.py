
from flask import Flask, request, render_template, redirect, session, flash, send_from_directory
import os
import sqlite3
import difflib
import shutil
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secure_secret_key'  # Secure secret key for session management

# Utility function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Enable dictionary-like access to rows
    return conn

@app.route('/')
def home():
    return render_template('home.html')  # Home page with student/teacher buttons

# Student and Teacher Login Pages
@app.route('/student_login')
def student_login_page():
    return render_template('login.html', role='student')

@app.route('/teacher_login')
def teacher_login_page():
    return render_template('login.html', role='teacher')

# Student Login Logic
@app.route('/student_login', methods=['POST'])
def student_login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        flash("Both email and password fields are required.", "error")
        return redirect('/student_login')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE email = ? AND password = ?", (email, password))
    student = cursor.fetchone()
    conn.close()

    if student:
        session['user_id'] = student['id']
        session['user_name'] = student['name']
        session['user_usn'] = student['usn']
        session['user_email'] = student['email']
        session['role'] = 'student'
        return redirect('/student_dashboard')
    else:
        flash("Invalid email or password.", "error")
        return redirect('/student_login')

# Teacher Login Logic
@app.route('/teacher_login', methods=['POST'])
def teacher_login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        flash("Both email and password fields are required.", "error")
        return redirect('/teacher_login')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teachers WHERE email = ? AND password = ?", (email, password))
    teacher = cursor.fetchone()
    conn.close()

    if teacher:
        session['user_id'] = teacher['teacher_id']
        session['user_name'] = teacher['name']
        session['user_email'] = teacher['email']
        session['role'] = 'teacher'
        return redirect('/teacher_dashboard')
    else:
        flash("Invalid email or password.", "error")
        return redirect('/teacher_login')

# Student Dashboard
@app.route('/student_dashboard')
def student_dashboard():
    if 'role' not in session or session['role'] != 'student':
        flash("Access denied.", "error")
        return redirect('/student_login')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, deadline FROM assignments")
    assignments = cursor.fetchall()

    # Fetch submitted assignment IDs for this student
    cursor.execute("SELECT assignment_id FROM submissions WHERE student_usn = ?", (session['user_usn'],))
    submitted_ids = [row['assignment_id'] for row in cursor.fetchall()]
    conn.close()

    # Mark each assignment with submission status
    assignment_list = []
    from datetime import datetime
    for a in assignments:
        is_submitted = a['id'] in submitted_ids
        is_past_deadline = datetime.strptime(a['deadline'], '%Y-%m-%d') < datetime.now()

        assignment_list.append({
            **dict(a),
            'is_submitted': is_submitted,
            'is_past_deadline': is_past_deadline
        })

    return render_template('student_dashboard.html',
        name=session['user_name'],
        usn=session['user_usn'],
        email=session['user_email'],
        assignments=assignment_list
    )


# Teacher Dashboard
@app.route('/teacher_dashboard')
def teacher_dashboard():
    if 'role' not in session or session['role'] != 'teacher':
        flash("Access denied. Please log in.", "error")
        return redirect('/teacher_login')

    teacher_name = session['user_name']
    teacher_email = session['user_email']
    tid=session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, deadline FROM assignments WHERE teacher_id = ?", (tid,))

    assignments = cursor.fetchall()
    conn.close()

    return render_template('teacher_dashboard.html', name=teacher_name, email=teacher_email, assignments=assignments)
app.config['UPLOAD_FOLDER'] = 'uploads'  
# Create Assignment (Only Teachers)
@app.route('/create_assignment', methods=['GET', 'POST'])
def create_assignment():
    if 'role' not in session or session['role'] != 'teacher':
        flash("Access denied. Please log in as a teacher.", "error")
        return redirect('/teacher_login')

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        deadline = request.form['deadline']

        if not title or not description or not deadline:
            flash("All fields are required.", "error")
            return redirect('/create_assignment')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
    "INSERT INTO assignments (title, description, deadline, teacher_id) VALUES (?, ?, ?, ?)",
    (title, description, deadline, session['user_id'])
)

        conn.commit()
        conn.close()

        flash(f"Assignment '{title}' created successfully!", "success")
        return redirect('/teacher_dashboard')

    return render_template('create_assignment.html')



from werkzeug.utils import secure_filename
from flask import jsonify
# Student submits assignment

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  # Absolute path
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/submit_assignment', methods=['POST'])
def submit_assignment():
    assignment_id = request.form.get('assignment_id')
    student_usn = session.get('user_usn')

    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'})

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check deadline
    cursor.execute("SELECT deadline FROM assignments WHERE id = ?", (assignment_id,))
    result = cursor.fetchone()
    if result and result["deadline"] < datetime.now().strftime("%Y-%m-%d %H:%M:%S"):
        conn.close()
        return jsonify({'success': False, 'error': 'Deadline passed'})

    # Check if already submitted
    cursor.execute(
        "SELECT * FROM submissions WHERE student_usn = ? AND assignment_id = ?",
        (student_usn, assignment_id)
    )
    if cursor.fetchone():
        conn.close()
        return jsonify({'success': False, 'error': 'Already submitted'})

    # Save file and insert
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    cursor.execute('''
        INSERT INTO submissions (student_usn, student_name, assignment_id, submission_filename, submission_date)
        VALUES (?, ?, ?, ?, datetime('now'))
    ''', (student_usn, session['user_name'], assignment_id, file_path))
    conn.commit()
    conn.close()

    return jsonify({'success': True})


#view submissions
@app.route('/view_submissions/<int:assignment_id>')
def view_submissions(assignment_id):
    if 'role' not in session or session['role'] != 'teacher':
        flash("Access denied.", "error")
        return redirect('/')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT  assignment_id,student_name,student_usn, submission_date,submission_filename FROM submissions WHERE assignment_id = ?", (assignment_id,))
    submissions = cursor.fetchall()
    conn.close()
    
    return render_template('view_submissions.html', submissions=submissions, assignment_id=assignment_id)
#view file

from flask import send_file 
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  # Absolute path
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/view_file/<filename>')
def view_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return "File not found", 404




# Plagiarism Check
@app.route('/check_plagiarism/<path:filename>')
def check_plagiarism(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(file_path):
        flash("File not found for plagiarism check.", "error")
        return redirect(request.referrer)

    with open(file_path, 'r', encoding='ISO-8859-1') as file:
        uploaded_text = file.read()

    # Example reference texts (replace with actual dataset later)
    reference_texts = [
        "This section presents a detailed low-level design of each major component of the Smart Diaper–based UTI Detection System. For each component, a functional description, activity flow, and the technologies or methods used are elaborated. The corresponding activity diagram visually explains the internal logic and data flow of each unit in the system architecture.",
        "The smart diaper sensor unit is responsible for detecting changes in the pH level of the urine. This pH sensor continuously monitors the moisture and chemical composition to determine if the conditions are indicative of a potential urinary tract infection (UTI). Once the sensor detects the pH value, it converts the chemical signal into an electrical signal using an onboard analog-to-digital converter or microcontroller. This electrical data is then packaged and transmitted wirelessly to the edge gateway via BLE (Bluetooth Low Energy) or another short-range protocol. The diagram above illustrates the basic flow: sensing the pH, converting it to an electrical signal, and transmitting the data for further analysis.",
        " Implement a client to consume methods from the WSDL service which are available over internet. Your client program should access the exposed methods in WSDL and perform necessary operations",
        "To address this gap, there is a growing need for a portable, real-time, and intelligent system that can continuously monitor ECG signals and accurately detect AF, even outside clinical settings. The  proposed intelligent telecardiology system that utilizes a wearable, wireless ECG device integrated with a mobile-based expert system and real-time alert capabilities for early AF detection and remote cardiac care.",
        "The Backend API Flow manages the core data operations and orchestrates communication between system components. It receives incoming API calls from the edge gateway, which typically originate from IoT sensors in the smart diaper. The incoming data is first parsed and validated to ensure correctness and integrity. "
        
    ]

    plagiarism_percentage = max(
        difflib.SequenceMatcher(None, uploaded_text, ref).ratio() for ref in reference_texts
    ) * 100

    plagiarism_result = f"Plagiarism Score: {round(plagiarism_percentage, 2)}%"
    if plagiarism_percentage > 50:
        plagiarism_result += " - High similarity detected!"

    return render_template('plagiarism_result.html', filename=filename, plagiarism_result=plagiarism_result)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
  