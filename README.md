# 📚 EduSubmit

A web-based assignment submission and plagiarism detection system built for educational institutions. Teachers can create assignments and review submissions; students can submit files and track deadlines — all in one place.

---

## 🌐 Live Demo

👉 **[https://edusubmit-yp09.onrender.com](https://edusubmit-yp09.onrender.com)**

> **Note:** Hosted on Render's free plan — may take 30–60 seconds to load on first visit (cold start).

---

## ✨ Features

### 👩‍🏫 Teacher
- Secure login portal
- Create assignments with title, description, and deadline
- View all student submissions per assignment
- Download submitted files (PDF, DOCX, TXT)
- Run plagiarism checks using TF-IDF cosine similarity

### 🎓 Student
- Secure login portal
- View all active assignments with deadlines
- Submit assignments (PDF, DOCX, TXT supported)
- See submission status (submitted / pending / deadline passed)
- Prevented from submitting after deadline or re-submitting

### 🔍 Plagiarism Detection
- Compares submitted file against all other submissions for the same assignment
- Uses TF-IDF vectorization + cosine similarity (scikit-learn)
- Severity levels: Original / Low / Moderate / Severe

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite (file-based) |
| ML / NLP | scikit-learn, scipy, numpy |
| File Parsing | PyPDF2 (PDF), python-docx (DOCX) |
| Server | Gunicorn |
| Frontend | HTML, CSS, Jinja2 templates |

---

## 🚀 Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/Shama-M113/EDUSUBMIT.git
cd EDUSUBMIT
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Seed the database
```bash
python load_student.py
python load_teachers.py
python load_assignments.py
python load_submissions.py
```

### 5. Run the app
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

---


## 📁 Project Structure

```
EDUSUBMIT/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── Procfile                # Gunicorn start command
├── render.yaml             # Render deployment config
├── database.db             # SQLite database (auto-generated)
├── load_student.py         # Seed students
├── load_teachers.py        # Seed teachers
├── load_assignments.py     # Seed assignments
├── load_submissions.py     # Seed submissions
├── templates/              # HTML templates (Jinja2)
│   ├── home.html
│   ├── login.html
│   ├── student_dashboard.html
│   ├── teacher_dashboard.html
│   ├── create_assignment.html
│   ├── view_submissions.html
│   ├── submit.html
│   ├── submit_confirm.html
│   └── plagiarism_result.html
└── static/
    └── images/
```


