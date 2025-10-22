"""
ANTI-PATTERN EXAMPLE - GRADES PAGE
This file demonstrates TERRIBLE practices:
- Everything mixed together (HTML, CSS, JS, SQL, Python)
- Business logic and validation in view function
- Create AND Delete operations crammed in the same function
- No MVC pattern
- Massive inline styles and scripts
- No code reuse
- Hardcoded database queries
- Poor performance (N+1 queries)
- No error handling
- Global state management
- Handling GET, POST (create), and POST (delete) in the same massive function
- No RESTful design
DO NOT USE THIS CODE IN REAL PROJECTS!
"""

import sqlite3
from flask import request

def render_grades_page():
    # ANTI-PATTERN: Handling both GET and POST in the same massive function!
    message = ""
    message_type = ""
    
    # ANTI-PATTERN: Business logic mixed directly in view
    if request.method == 'POST':
        # ANTI-PATTERN: Multiple different actions in one handler
        action = request.form.get('action', 'create')
        
        if action == 'delete':
            # ANTI-PATTERN: Delete logic crammed into the same function!
            delete_id = request.form.get('delete_id', '')
            
            if not delete_id:
                message = "Error: No grade ID provided for deletion"
                message_type = "error"
            else:
                # ANTI-PATTERN: Direct database deletion without service layer
                conn = sqlite3.connect("students.db")
                c = conn.cursor()
                
                # ANTI-PATTERN: No verification before deletion
                try:
                    c.execute("DELETE FROM grades WHERE id = ?", (int(delete_id),))
                    
                    if c.rowcount > 0:
                        conn.commit()
                        message = "Grade deleted successfully! 🗑️"
                        message_type = "success"
                    else:
                        message = "Error: Grade not found"
                        message_type = "error"
                except Exception as e:
                    message = f"Error deleting grade: {str(e)}"
                    message_type = "error"
                finally:
                    conn.close()
        else:
            # ANTI-PATTERN: Create logic
            # ANTI-PATTERN: No validation layer, just grab form data
            student_id = request.form.get('student_id', '')
            course = request.form.get('course', '')
            grade = request.form.get('grade', '')
            semester = request.form.get('semester', '')
            credits = request.form.get('credits', '')
            
            # ANTI-PATTERN: Validation logic in view function instead of separate validator
            errors = []
            if not student_id:
                errors.append("Student is required")
            if not course or len(course) < 2:
                errors.append("Course name must be at least 2 characters")
            if not grade:
                errors.append("Grade is required")
            valid_grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F']
            if grade and grade not in valid_grades:
                errors.append("Invalid grade")
            if not semester:
                errors.append("Semester is required")
            if credits:
                try:
                    credits_int = int(credits)
                    if credits_int < 1 or credits_int > 6:
                        errors.append("Credits must be between 1 and 6")
                except:
                    errors.append("Credits must be a number")
            
            if errors:
                message = "Errors: " + "; ".join(errors)
                message_type = "error"
            else:
                # ANTI-PATTERN: Direct database manipulation in view function
                conn = sqlite3.connect("students.db")
                c = conn.cursor()
                
                # ANTI-PATTERN: No try-except for database errors
                c.execute("INSERT INTO grades (student_id, course, grade, semester, credits) VALUES (?, ?, ?, ?, ?)",
                         (int(student_id), course, grade, semester, int(credits) if credits else 3))
                conn.commit()
                conn.close()
                
                message = "Grade added successfully! ✅"
                message_type = "success"
    
    # ANTI-PATTERN: Getting parameters directly in page rendering function
    student_filter = request.args.get('student', '')
    course_filter = request.args.get('course', '')
    semester_filter = request.args.get('semester', '')
    
    # ANTI-PATTERN: Multiple database connections instead of connection pooling
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    
    # ANTI-PATTERN: Building complex queries in the view function
    query = "SELECT g.id, g.student_id, s.name, g.course, g.grade, g.semester, g.credits FROM grades g JOIN students s ON g.student_id = s.id WHERE 1=1"
    
    if student_filter:
        query += " AND s.name LIKE '%" + student_filter + "%'"
    if course_filter:
        query += " AND g.course LIKE '%" + course_filter + "%'"
    if semester_filter:
        query += " AND g.semester = '" + semester_filter + "'"
    
    c.execute(query)
    grades = c.fetchall()
    
    # Get all students for dropdown
    c.execute("SELECT id, name FROM students ORDER BY name")
    all_students = c.fetchall()
    
    # Get all unique semesters
    c.execute("SELECT DISTINCT semester FROM grades ORDER BY semester")
    semesters = c.fetchall()
    
    # Get unique courses for datalist
    c.execute("SELECT DISTINCT course FROM grades ORDER BY course")
    courses = c.fetchall()
    
    conn.close()
    
    # ANTI-PATTERN: Calculate statistics in Python instead of SQL
    total_credits = sum(g[6] for g in grades)
    grade_counts = {}
    for grade in grades:
        g = grade[4]
        if g in grade_counts:
            grade_counts[g] += 1
        else:
            grade_counts[g] = 1
    
    # ANTI-PATTERN: Massive HTML string generation
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Grades - HORRIBLE EXAMPLE</title>
    <meta charset="UTF-8">
    
    <!-- ANTI-PATTERN: All CSS inline in the same file -->
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(120deg, #89f7fe 0%, #66a6ff 100%);
            min-height: 100vh;
            padding: 20px;
            background-attachment: fixed;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            text-align: center;
        }
        
        .header h1 {
            font-size: 42px;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .warning-banner {
            background: #ff3333;
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
            font-weight: bold;
            font-size: 20px;
            animation: pulse 2s infinite;
            box-shadow: 0 5px 15px rgba(255,0,0,0.3);
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.02); }
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        
        .navigation {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        
        .nav-btn {
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            transition: all 0.3s;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .nav-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.2);
        }
        
        .stats-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
        }
        
        .stat-card h3 {
            font-size: 40px;
            margin-bottom: 10px;
        }
        
        .stat-card p {
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .filters {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
            border: 2px solid #e9ecef;
        }
        
        .filter-row {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }
        
        .filter-group {
            flex: 1;
            min-width: 200px;
        }
        
        .filter-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #333;
        }
        
        .filter-group input,
        .filter-group select {
            width: 100%;
            padding: 12px;
            border: 2px solid #dee2e6;
            border-radius: 6px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        
        .filter-group input:focus,
        .filter-group select:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            text-transform: uppercase;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-primary:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .btn-secondary {
            background: #6c757d;
            color: white;
        }
        
        .btn-secondary:hover {
            background: #5a6268;
        }
        
        .btn-danger {
            background: #dc3545;
            color: white;
        }
        
        .btn-danger:hover {
            background: #c82333;
        }
        
        .btn-success {
            background: #28a745;
            color: white;
        }
        
        .btn-success:hover {
            background: #218838;
        }
        
        .grades-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin-top: 20px;
            box-shadow: 0 2px 15px rgba(0,0,0,0.1);
            border-radius: 10px;
            overflow: hidden;
        }
        
        .grades-table thead {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .grades-table thead th {
            padding: 18px 15px;
            text-align: left;
            color: white;
            font-weight: bold;
            text-transform: uppercase;
            font-size: 13px;
            letter-spacing: 1px;
            cursor: pointer;
            user-select: none;
        }
        
        .grades-table thead th:hover {
            background: rgba(255,255,255,0.1);
        }
        
        .grades-table tbody tr {
            border-bottom: 1px solid #e9ecef;
            transition: all 0.3s;
        }
        
        .grades-table tbody tr:hover {
            background: #f8f9fa;
            transform: scale(1.01);
        }
        
        .grades-table tbody tr:nth-child(even) {
            background: #fafbfc;
        }
        
        .grades-table tbody tr:nth-child(even):hover {
            background: #f1f3f5;
        }
        
        .grades-table td {
            padding: 15px;
            color: #333;
        }
        
        .grade-badge {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 14px;
            text-align: center;
            min-width: 50px;
        }
        
        .grade-A { background: #28a745; color: white; }
        .grade-A- { background: #5cb85c; color: white; }
        .grade-B-plus { background: #17a2b8; color: white; }
        .grade-B { background: #ffc107; color: black; }
        .grade-B- { background: #fd7e14; color: white; }
        .grade-C-plus { background: #ff851b; color: white; }
        .grade-C { background: #dc3545; color: white; }
        .grade-C- { background: #c82333; color: white; }
        .grade-D { background: #6c757d; color: white; }
        .grade-F { background: #343a40; color: white; }
        
        .chart-container {
            margin: 30px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        
        .chart-title {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #333;
        }
        
        .bar-chart {
            display: flex;
            align-items: flex-end;
            height: 200px;
            gap: 10px;
        }
        
        .bar {
            flex: 1;
            background: linear-gradient(to top, #667eea 0%, #764ba2 100%);
            border-radius: 5px 5px 0 0;
            position: relative;
            transition: all 0.3s;
            min-height: 20px;
        }
        
        .bar:hover {
            opacity: 0.8;
            transform: scaleY(1.05);
        }
        
        .bar-label {
            position: absolute;
            bottom: -25px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 12px;
            font-weight: bold;
        }
        
        .bar-value {
            position: absolute;
            top: -25px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 14px;
            font-weight: bold;
            color: #667eea;
        }
        
        .action-buttons {
            display: flex;
            gap: 10px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        
        .tooltip {
            position: relative;
            display: inline-block;
        }
        
        .tooltip .tooltiptext {
            visibility: hidden;
            width: 200px;
            background-color: #555;
            color: #fff;
            text-align: center;
            border-radius: 6px;
            padding: 10px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -100px;
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 50px;
            font-size: 20px;
            color: #667eea;
        }
        
        .spinner {
            border: 5px solid #f3f3f3;
            border-top: 5px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .no-results {
            text-align: center;
            padding: 50px;
            color: #999;
            font-size: 18px;
        }
        
        .footer {
            margin-top: 30px;
            text-align: center;
            color: #6c757d;
            font-size: 14px;
            padding: 20px;
            border-top: 2px solid #e9ecef;
        }
        
        .message {
            padding: 15px;
            margin: 20px 0;
            border-radius: 8px;
            font-weight: bold;
            text-align: center;
            animation: fadeIn 0.5s;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .message-success {
            background: #d4edda;
            color: #155724;
            border: 2px solid #c3e6cb;
        }
        
        .message-error {
            background: #f8d7da;
            color: #721c24;
            border: 2px solid #f5c6cb;
        }
        
        .create-grade-form {
            background: linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 100%);
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
            border: 3px solid #00bcd4;
            box-shadow: 0 5px 15px rgba(0,188,212,0.2);
        }
        
        .create-grade-form h3 {
            margin-top: 0;
            margin-bottom: 20px;
            color: #00695c;
            font-size: 22px;
        }
        
        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 15px;
        }
        
        .form-group {
            display: flex;
            flex-direction: column;
        }
        
        .form-group label {
            margin-bottom: 5px;
            font-weight: bold;
            color: #00695c;
            font-size: 14px;
        }
        
        .form-group input,
        .form-group select {
            padding: 10px;
            border: 2px solid #b2ebf2;
            border-radius: 5px;
            font-size: 14px;
        }
        
        .form-group input:focus,
        .form-group select:focus {
            outline: none;
            border-color: #00bcd4;
            box-shadow: 0 0 5px rgba(0,188,212,0.5);
        }
        
        .btn-add-grade {
            background: linear-gradient(135deg, #00bcd4 0%, #00acc1 100%);
            color: white;
            padding: 14px 35px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            text-transform: uppercase;
        }
        
        .btn-add-grade:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 20px rgba(0,188,212,0.4);
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎓 Student Grades Dashboard</h1>
        <p>Academic Performance Tracking System</p>
    </div>
    
    <div class="warning-banner">
        ⚠️ ANTI-PATTERN EXAMPLE - DO NOT COPY THIS ARCHITECTURE ⚠️
    </div>
    
    <div class="container">
        <div class="navigation">
            <a href="/" class="nav-btn">🏠 Home</a>
            <a href="/students" class="nav-btn">👥 Students</a>
            <a href="/grades" class="nav-btn">📊 Grades (Current)</a>
        </div>"""
    
    # ANTI-PATTERN: Generating conditional HTML in Python
    if message:
        html += f"""
        <div class="message message-{message_type}">
            {message}
        </div>"""
    
    html += """
        
        <!-- ANTI-PATTERN: Create form mixed with everything else -->
        <div class="create-grade-form">
            <h3>➕ Add New Grade Entry</h3>
            <form method="POST" action="/grades">
                <div class="form-grid">
                    <div class="form-group">
                        <label>Student *</label>
                        <select name="student_id" required>
                            <option value="">-- Select Student --</option>"""
    
    # ANTI-PATTERN: Building select options in Python
    for student in all_students:
        html += f"""
                            <option value="{student[0]}">{student[1]}</option>"""
    
    html += """
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Course *</label>
                        <input type="text" name="course" placeholder="e.g. Data Structures" required list="course-list">
                        <datalist id="course-list">"""
    
    # ANTI-PATTERN: More options in Python
    for course in courses:
        html += f"""
                            <option value="{course[0]}">"""
    
    html += """
                        </datalist>
                    </div>
                    
                    <div class="form-group">
                        <label>Grade *</label>
                        <select name="grade" required>
                            <option value="">-- Select Grade --</option>
                            <option value="A">A</option>
                            <option value="A-">A-</option>
                            <option value="B+">B+</option>
                            <option value="B">B</option>
                            <option value="B-">B-</option>
                            <option value="C+">C+</option>
                            <option value="C">C</option>
                            <option value="C-">C-</option>
                            <option value="D">D</option>
                            <option value="F">F</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Semester *</label>
                        <input type="text" name="semester" placeholder="e.g. Fall 2024" required list="semester-list">
                        <datalist id="semester-list">"""
    
    # ANTI-PATTERN: Even more datalist in Python
    for semester in semesters:
        html += f"""
                            <option value="{semester[0]}">"""
    
    html += """
                        </datalist>
                    </div>
                    
                    <div class="form-group">
                        <label>Credits</label>
                        <input type="number" name="credits" placeholder="3" min="1" max="6" value="3">
                    </div>
                </div>
                
                <button type="submit" class="btn-add-grade">✅ Add Grade</button>
            </form>
        </div>
        
        <div class="stats-container">
            <div class="stat-card">
                <h3>""" + str(len(grades)) + """</h3>
                <p>Total Grades</p>
            </div>
            <div class="stat-card">
                <h3>""" + str(total_credits) + """</h3>
                <p>Total Credits</p>
            </div>
            <div class="stat-card">
                <h3>""" + str(len(all_students)) + """</h3>
                <p>Students</p>
            </div>
            <div class="stat-card">
                <h3>""" + str(len(semesters)) + """</h3>
                <p>Semesters</p>
            </div>
        </div>
        
        <div class="filters">
            <form method="GET" action="/grades">
                <div class="filter-row">
                    <div class="filter-group">
                        <label>🔍 Search Student</label>
                        <input type="text" name="student" placeholder="Enter student name..." value\"""" + student_filter + """">
                    </div>
                    
                    <div class="filter-group">
                        <label>📚 Search Course</label>
                        <input type="text" name="course" placeholder="Enter course name..." value\"""" + course_filter + """">
                    </div>
                    
                    <div class="filter-group">
                        <label>📅 Semester</label>
                        <select name="semester">
                            <option value="">All Semesters</option>
"""
    
    # ANTI-PATTERN: More HTML generation in loops
    for semester in semesters:
        selected = "selected" if semester[0] == semester_filter else ""
        html += f'                            <option value="{semester[0]}" {selected}>{semester[0]}</option>\n'
    
    html += """
                        </select>
                    </div>
                    
                    <div class="filter-group" style="display: flex; gap: 10px; align-items: flex-end;">
                        <button type="submit" class="btn btn-primary">🔍 Filter</button>
                        <button type="button" class="btn btn-secondary" onclick="clearFilters()">🔄 Reset</button>
                    </div>
                </div>
            </form>
        </div>
        
        <div class="chart-container">
            <div class="chart-title">📊 Grade Distribution</div>
            <div class="bar-chart" id="gradeChart">
"""
    
    # ANTI-PATTERN: Generating chart in Python/HTML
    grade_order = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F']
    max_count = max(grade_counts.values()) if grade_counts else 1
    
    for grade in grade_order:
        count = grade_counts.get(grade, 0)
        height = (count / max_count * 100) if count > 0 else 5
        html += f"""
                <div class="bar" style="height: {height}%;">
                    <span class="bar-value">{count}</span>
                    <span class="bar-label">{grade}</span>
                </div>
"""
    
    html += """
            </div>
        </div>
        
        <div class="action-buttons">
            <button class="btn btn-success" onclick="exportToCSV()">💾 Export CSV</button>
            <button class="btn btn-primary" onclick="generateReport()">📄 Generate Report</button>
            <button class="btn btn-secondary" onclick="printGrades()">🖨️ Print</button>
            <button class="btn btn-danger" onclick="deleteSelected()">🗑️ Delete Selected</button>
        </div>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Loading grades...</p>
        </div>
        
        <table class="grades-table" id="gradesTable">
            <thead>
                <tr>
                    <th><input type="checkbox" id="selectAll" onclick="toggleSelectAll()"></th>
                    <th onclick="sortTableByColumn(0)">ID ↕️</th>
                    <th onclick="sortTableByColumn(1)">Student Name ↕️</th>
                    <th onclick="sortTableByColumn(2)">Course ↕️</th>
                    <th onclick="sortTableByColumn(3)">Grade ↕️</th>
                    <th onclick="sortTableByColumn(4)">Semester ↕️</th>
                    <th onclick="sortTableByColumn(5)">Credits ↕️</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
"""
    
    # ANTI-PATTERN: Generating table rows in Python
    if not grades:
        html += """
                <tr>
                    <td colspan="8" class="no-results">
                        📭 No grades found matching your criteria
                    </td>
                </tr>
"""
    else:
        for grade in grades:
            grade_class = f"grade-{grade[4].replace('+', '-plus').replace('-', '-')}" if grade[4] else "grade-F"
            html += f"""
                <tr>
                    <td><input type="checkbox" class="grade-checkbox" value="{grade[0]}"></td>
                    <td>{grade[0]}</td>
                    <td><strong>{grade[2]}</strong></td>
                    <td>{grade[3]}</td>
                    <td><span class="grade-badge {grade_class}">{grade[4]}</span></td>
                    <td>{grade[5]}</td>
                    <td>{grade[6]}</td>
                    <td>
                        <button class="btn btn-primary" style="padding: 5px 10px;" onclick="editGrade({grade[0]})">✏️</button>
                        <button class="btn btn-danger" style="padding: 5px 10px;" onclick="deleteGrade({grade[0]})">🗑️</button>
                    </td>
                </tr>
"""
    
    html += """
            </tbody>
        </table>
        
        <div class="footer">
            <p>© 2025 Terrible Student Management System | This is an ANTI-PATTERN example</p>
            <p>Total Records: """ + str(len(grades)) + """ | Last Updated: """ + "October 21, 2025" + """</p>
        </div>
    </div>
    
    <!-- ANTI-PATTERN: Massive inline JavaScript -->
    <script>
        // ANTI-PATTERN: Global variables without namespacing
        var allGrades = [
"""
    
    # ANTI-PATTERN: Embedding database data in JavaScript
    for i, grade in enumerate(grades):
        # ANTI-PATTERN: No proper escaping for special characters
        student_name = str(grade[2]).replace('"', '\\"').replace("'", "\\'")
        course_name = str(grade[3]).replace('"', '\\"').replace("'", "\\'")
        grade_value = str(grade[4]).replace('"', '\\"').replace("'", "\\'")
        semester_value = str(grade[5]).replace('"', '\\"').replace("'", "\\'")
        html += f"""            {{id: {grade[0]}, studentId: {grade[1]}, studentName: "{student_name}", course: "{course_name}", grade: "{grade_value}", semester: "{semester_value}", credits: {grade[6]}}}"""
        if i < len(grades) - 1:
            html += ",\n"
        else:
            html += "\n"
    
    html += """
        ];
        
        var sortDirection = 1;
        var lastSortColumn = -1;
        
        // ANTI-PATTERN: Huge function without proper modularization
        function sortTableByColumn(columnIndex) {
            var table = document.getElementById("gradesTable");
            var tbody = table.querySelector("tbody");
            var rows = Array.from(tbody.querySelectorAll("tr"));
            
            if (lastSortColumn === columnIndex) {
                sortDirection *= -1;
            } else {
                sortDirection = 1;
                lastSortColumn = columnIndex;
            }
            
            rows.sort(function(a, b) {
                var aValue = a.cells[columnIndex + 1].textContent.trim();
                var bValue = b.cells[columnIndex + 1].textContent.trim();
                
                var aNum = parseFloat(aValue);
                var bNum = parseFloat(bValue);
                
                if (!isNaN(aNum) && !isNaN(bNum)) {
                    return (aNum - bNum) * sortDirection;
                }
                
                return aValue.localeCompare(bValue) * sortDirection;
            });
            
            tbody.innerHTML = "";
            rows.forEach(function(row) {
                tbody.appendChild(row);
            });
            
            console.log("Sorted by column " + columnIndex + " in direction " + sortDirection);
        }
        
        // ANTI-PATTERN: Using alerts instead of proper UI
        function editGrade(gradeId) {
            var grade = allGrades.find(function(g) { return g.id === gradeId; });
            if (grade) {
                var newGrade = prompt("Enter new grade for " + grade.studentName + " in " + grade.course + ":", grade.grade);
                if (newGrade) {
                    alert("Edit functionality not implemented in this demo!");
                    console.log("Would update grade " + gradeId + " to: " + newGrade);
                }
            }
        }
        
        function deleteGrade(gradeId) {
            var grade = allGrades.find(function(g) { return g.id === gradeId; });
            if (grade && confirm("Are you sure you want to delete this grade record?\\n\\n" + grade.studentName + " - " + grade.course + " (" + grade.grade + ")")) {
                // ANTI-PATTERN: Creating and submitting form dynamically via JavaScript
                var form = document.createElement('form');
                form.method = 'POST';
                form.action = '/grades';
                
                var actionInput = document.createElement('input');
                actionInput.type = 'hidden';
                actionInput.name = 'action';
                actionInput.value = 'delete';
                form.appendChild(actionInput);
                
                var idInput = document.createElement('input');
                idInput.type = 'hidden';
                idInput.name = 'delete_id';
                idInput.value = gradeId;
                form.appendChild(idInput);
                
                document.body.appendChild(form);
                form.submit();
            }
        }
        
        function toggleSelectAll() {
            var selectAll = document.getElementById("selectAll");
            var checkboxes = document.querySelectorAll(".grade-checkbox");
            checkboxes.forEach(function(checkbox) {
                checkbox.checked = selectAll.checked;
            });
        }
        
        function deleteSelected() {
            var checkboxes = document.querySelectorAll(".grade-checkbox:checked");
            if (checkboxes.length === 0) {
                alert("Please select grades to delete");
                return;
            }
            
            if (confirm("Delete " + checkboxes.length + " selected grade(s)?")) {
                alert("Bulk delete functionality not implemented in this demo!");
                var ids = Array.from(checkboxes).map(function(cb) { return cb.value; });
                console.log("Would delete grades: " + ids.join(", "));
            }
        }
        
        function clearFilters() {
            window.location.href = '/grades';
        }
        
        // ANTI-PATTERN: Client-side CSV generation with poor error handling
        function exportToCSV() {
            var csv = "ID,Student ID,Student Name,Course,Grade,Semester,Credits\\n";
            
            allGrades.forEach(function(grade) {
                csv += grade.id + ",";
                csv += grade.studentId + ",";
                csv += '"' + grade.studentName + '",';
                csv += '"' + grade.course + '",';
                csv += grade.grade + ",";
                csv += grade.semester + ",";
                csv += grade.credits + "\\n";
            });
            
            var blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
            var link = document.createElement("a");
            var url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", "grades_export.csv");
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            alert("CSV file downloaded!");
        }
        
        function generateReport() {
            alert("Generating report...\\n\\nThis feature is not implemented in this demo.\\n\\nIn a real system, this would generate a comprehensive PDF report.");
        }
        
        function printGrades() {
            window.print();
        }
        
        // ANTI-PATTERN: Manipulating DOM on load without proper initialization
        window.onload = function() {
            console.log("Grades page loaded with " + allGrades.length + " records");
            
            // ANTI-PATTERN: Animate elements individually instead of using CSS classes
            var rows = document.querySelectorAll("tbody tr");
            rows.forEach(function(row, index) {
                setTimeout(function() {
                    row.style.opacity = "0";
                    row.style.transform = "translateX(-50px)";
                    row.style.transition = "all 0.5s";
                    setTimeout(function() {
                        row.style.opacity = "1";
                        row.style.transform = "translateX(0)";
                    }, 50);
                }, index * 30);
            });
            
            // ANTI-PATTERN: Calculating stats in JavaScript that should be done server-side
            calculateStatistics();
        };
        
        function calculateStatistics() {
            var totalA = 0, totalB = 0, totalC = 0, totalOther = 0;
            
            allGrades.forEach(function(grade) {
                if (grade.grade.startsWith('A')) totalA++;
                else if (grade.grade.startsWith('B')) totalB++;
                else if (grade.grade.startsWith('C')) totalC++;
                else totalOther++;
            });
            
            console.log("Grade Statistics:");
            console.log("A grades: " + totalA);
            console.log("B grades: " + totalB);
            console.log("C grades: " + totalC);
            console.log("Other: " + totalOther);
        }
        
        // ANTI-PATTERN: Polling for updates instead of WebSockets
        setInterval(function() {
            console.log("Checking for updates... (not really)");
        }, 10000);
        
        // ANTI-PATTERN: Adding event listeners in multiple places
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'e') {
                e.preventDefault();
                exportToCSV();
            }
            if (e.ctrlKey && e.key === 'p') {
                e.preventDefault();
                printGrades();
            }
        });
        
        // ANTI-PATTERN: Global error handler that just logs
        window.onerror = function(msg, url, lineNo, columnNo, error) {
            console.log("Error: " + msg);
            return false;
        };
        
        // ANTI-PATTERN: Unnecessary animations that consume resources
        setInterval(function() {
            var statCards = document.querySelectorAll('.stat-card');
            var randomCard = statCards[Math.floor(Math.random() * statCards.length)];
            if (randomCard) {
                randomCard.style.transition = 'transform 0.3s';
                randomCard.style.transform = 'scale(1.05)';
                setTimeout(function() {
                    randomCard.style.transform = 'scale(1)';
                }, 300);
            }
        }, 3000);
        
        // ANTI-PATTERN: Adding more functionality without proper architecture
        function highlightStudent(studentName) {
            var rows = document.querySelectorAll('tbody tr');
            rows.forEach(function(row) {
                if (row.textContent.includes(studentName)) {
                    row.style.background = '#ffffcc';
                    setTimeout(function() {
                        row.style.background = '';
                    }, 2000);
                }
            });
        }
        
        // ANTI-PATTERN: Memory leaks by not cleaning up event listeners
        document.querySelectorAll('.grade-checkbox').forEach(function(checkbox) {
            checkbox.addEventListener('change', function() {
                console.log('Checkbox changed: ' + this.value);
            });
        });
    </script>
    
    <!-- ANTI-PATTERN: More styles after JavaScript -->
    <style>
        @media print {
            .filters, .action-buttons, .navigation, .warning-banner {
                display: none !important;
            }
            .container {
                box-shadow: none;
            }
        }
        
        @media (max-width: 768px) {
            .stats-container {
                grid-template-columns: 1fr;
            }
            .filter-row {
                flex-direction: column;
            }
            .grades-table {
                font-size: 12px;
            }
        }
    </style>
</body>
</html>
"""
    
    return html

