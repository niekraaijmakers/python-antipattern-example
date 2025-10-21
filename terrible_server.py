#!/usr/bin/env python3
"""
ANTI-PATTERN EXAMPLE - DO NOT USE IN PRODUCTION!
This is intentionally bad code for educational purposes.
"""

from flask import Flask, request, Response
import sqlite3
import os

app = Flask(__name__)

# ANTI-PATTERN: Hardcoded database path
db_path = "students.db"

# Initialize database with sample data
def init_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Create tables
    c.execute('''DROP TABLE IF EXISTS students''')
    c.execute('''DROP TABLE IF EXISTS grades''')
    
    c.execute('''CREATE TABLE students (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        age INTEGER,
        major TEXT,
        gpa REAL
    )''')
    
    c.execute('''CREATE TABLE grades (
        id INTEGER PRIMARY KEY,
        student_id INTEGER,
        course TEXT,
        grade TEXT,
        semester TEXT,
        credits INTEGER
    )''')
    
    # Insert sample students
    students = [
        (1, "Alice Johnson", "alice@email.com", 20, "Computer Science", 3.8),
        (2, "Bob Smith", "bob@email.com", 22, "Mathematics", 3.5),
        (3, "Charlie Brown", "charlie@email.com", 21, "Physics", 3.9),
        (4, "Diana Prince", "diana@email.com", 19, "Engineering", 3.7),
        (5, "Edward Norton", "edward@email.com", 23, "Computer Science", 3.2),
        (6, "Fiona Apple", "fiona@email.com", 20, "Biology", 3.6),
        (7, "George Lucas", "george@email.com", 22, "Film Studies", 3.4),
        (8, "Hannah Montana", "hannah@email.com", 21, "Music", 3.9),
        (9, "Ian McKellen", "ian@email.com", 24, "Theater", 3.1),
        (10, "Julia Roberts", "julia@email.com", 20, "Chemistry", 3.8)
    ]
    
    c.executemany('INSERT INTO students VALUES (?,?,?,?,?,?)', students)
    
    # Insert sample grades
    grades = [
        (1, 1, "Introduction to Programming", "A", "Fall 2024", 4),
        (2, 1, "Data Structures", "A-", "Fall 2024", 4),
        (3, 1, "Web Development", "B+", "Spring 2024", 3),
        (4, 2, "Calculus I", "B", "Fall 2024", 4),
        (5, 2, "Linear Algebra", "A-", "Fall 2024", 3),
        (6, 3, "Quantum Mechanics", "A", "Fall 2024", 4),
        (7, 3, "Classical Mechanics", "A", "Spring 2024", 4),
        (8, 4, "Thermodynamics", "B+", "Fall 2024", 3),
        (9, 4, "Circuit Design", "A-", "Fall 2024", 4),
        (10, 5, "Operating Systems", "C+", "Fall 2024", 4),
        (11, 5, "Computer Networks", "B", "Spring 2024", 3),
        (12, 6, "Molecular Biology", "A-", "Fall 2024", 4),
        (13, 6, "Genetics", "A", "Spring 2024", 4),
        (14, 7, "Film History", "B+", "Fall 2024", 3),
        (15, 7, "Screenwriting", "B", "Spring 2024", 3),
        (16, 8, "Music Theory", "A", "Fall 2024", 4),
        (17, 8, "Performance Art", "A", "Fall 2024", 2),
        (18, 9, "Shakespeare Studies", "C", "Fall 2024", 3),
        (19, 9, "Modern Drama", "B-", "Spring 2024", 3),
        (20, 10, "Organic Chemistry", "A-", "Fall 2024", 4),
        (21, 10, "Analytical Chemistry", "A", "Spring 2024", 3)
    ]
    
    c.executemany('INSERT INTO grades VALUES (?,?,?,?,?,?)', grades)
    
    conn.commit()
    conn.close()

# Initialize database on startup
if not os.path.exists(db_path):
    init_db()

@app.route('/')
def index():
    return '''
    <html>
    <head><title>Student Management System</title></head>
    <body style="font-family: Arial; padding: 50px; background: #f0f0f0;">
        <h1>Terrible Student Management System</h1>
        <h2>ANTI-PATTERN EXAMPLE - DO NOT COPY THIS CODE!</h2>
        <div>
            <a href="/students" style="padding: 10px; background: blue; color: white; text-decoration: none; margin: 10px;">View Students</a>
            <a href="/grades" style="padding: 10px; background: green; color: white; text-decoration: none; margin: 10px;">View Grades</a>
        </div>
    </body>
    </html>
    '''

# Import the horrible route files
from student_page import render_student_page
from grades_page import render_grades_page

@app.route('/students')
def students():
    return render_student_page()

@app.route('/grades')
def grades():
    return render_grades_page()

if __name__ == '__main__':
    app.run(debug=True, port=5000)

