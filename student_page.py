"""
ANTI-PATTERN EXAMPLE - STUDENT DATA PAGE
This file demonstrates TERRIBLE practices:
- Mixing HTML, CSS, JavaScript, and SQL in one file
- Business logic mixed with presentation logic
- Create AND Delete operations in the same function
- Validation logic in the view function
- No separation of concerns
- Inline styles everywhere
- Repetitive code
- No proper error handling
- Hardcoded values
- No templating engine
- Giant functions
- Poor variable naming
- Handling GET, POST (create), and POST (delete) in the same function
- No RESTful design
DO NOT USE THIS CODE IN REAL PROJECTS!
"""

import sqlite3
from flask import request

def render_student_page():
    # ANTI-PATTERN: Handling both GET and POST in the same function!
    message = ""
    message_type = ""
    
    # ANTI-PATTERN: Business logic mixed with view logic
    if request.method == 'POST':
        # ANTI-PATTERN: Multiple actions handled in one function without proper routing
        action = request.form.get('action', 'create')
        
        if action == 'delete':
            # ANTI-PATTERN: Delete logic mixed in the same function!
            delete_id = request.form.get('delete_id', '')
            
            if not delete_id:
                message = "Error: No student ID provided for deletion"
                message_type = "error"
            else:
                # ANTI-PATTERN: Direct database deletion in view function
                conn = sqlite3.connect("students.db")
                c = conn.cursor()
                
                # ANTI-PATTERN: No check if student exists before deleting
                # ANTI-PATTERN: Deleting without checking for foreign key constraints
                try:
                    # First delete associated grades
                    c.execute("DELETE FROM grades WHERE student_id = ?", (int(delete_id),))
                    # Then delete the student
                    c.execute("DELETE FROM students WHERE id = ?", (int(delete_id),))
                    
                    if c.rowcount > 0:
                        conn.commit()
                        message = "Student deleted successfully! 🗑️"
                        message_type = "success"
                    else:
                        message = "Error: Student not found"
                        message_type = "error"
                except Exception as e:
                    message = f"Error deleting student: {str(e)}"
                    message_type = "error"
                finally:
                    conn.close()
        else:
            # ANTI-PATTERN: Create logic
            # ANTI-PATTERN: Getting form data without validation
            name = request.form.get('name', '')
            email = request.form.get('email', '')
            age = request.form.get('age', '')
            major = request.form.get('major', '')
            gpa = request.form.get('gpa', '')
            
            # ANTI-PATTERN: Validation logic in the view function
            errors = []
            if not name or len(name) < 2:
                errors.append("Name must be at least 2 characters")
            if not email or '@' not in email:
                errors.append("Invalid email")
            if age:
                try:
                    age_int = int(age)
                    if age_int < 16 or age_int > 100:
                        errors.append("Age must be between 16 and 100")
                except:
                    errors.append("Age must be a number")
            if gpa:
                try:
                    gpa_float = float(gpa)
                    if gpa_float < 0 or gpa_float > 4.0:
                        errors.append("GPA must be between 0 and 4.0")
                except:
                    errors.append("GPA must be a number")
            
            if errors:
                message = "Errors: " + ", ".join(errors)
                message_type = "error"
            else:
                # ANTI-PATTERN: Database operations in view function
                conn = sqlite3.connect("students.db")
                c = conn.cursor()
                
                # ANTI-PATTERN: No error handling for database operations
                c.execute("INSERT INTO students (name, email, age, major, gpa) VALUES (?, ?, ?, ?, ?)",
                         (name, email, int(age) if age else None, major, float(gpa) if gpa else None))
                conn.commit()
                conn.close()
                
                message = "Student created successfully!"
                message_type = "success"
    
    # ANTI-PATTERN: Getting parameters directly in page rendering function
    search = request.args.get('search', '')
    filter_major = request.args.get('major', '')
    
    # ANTI-PATTERN: Opening database connection in view function
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    
    # ANTI-PATTERN: Building queries in the page rendering function
    if search:
        query = "SELECT * FROM students WHERE name LIKE '%" + search + "%'"
    elif filter_major:
        query = "SELECT * FROM students WHERE major = '" + filter_major + "'"
    else:
        query = "SELECT * FROM students"
    
    c.execute(query)
    students = c.fetchall()
    
    # Get all majors for filter
    c.execute("SELECT DISTINCT major FROM students")
    majors = c.fetchall()
    
    conn.close()
    
    # ANTI-PATTERN: Generating HTML in Python code!
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Data - TERRIBLE EXAMPLE</title>
    
    <!-- ANTI-PATTERN: Inline styles instead of separate CSS file -->
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #FFA07A);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
        }
        
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: white;
            margin-top: 20px;
            margin-bottom: 20px;
            box-shadow: 0 0 20px rgba(0,0,0,0.3);
            border-radius: 10px;
        }
        
        h1 {
            color: #333;
            text-align: center;
            font-size: 36px;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        .warning {
            background: #ff4444;
            color: white;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
            font-weight: bold;
            font-size: 18px;
            animation: blink 2s infinite;
        }
        
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .controls {
            background: #f8f8f8;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 5px;
            border: 2px solid #ddd;
        }
        
        input[type="text"] {
            padding: 10px;
            font-size: 16px;
            border: 2px solid #4ECDC4;
            border-radius: 5px;
            width: 300px;
            margin-right: 10px;
        }
        
        select {
            padding: 10px;
            font-size: 16px;
            border: 2px solid #45B7D1;
            border-radius: 5px;
            margin-right: 10px;
            background: white;
        }
        
        button {
            padding: 10px 20px;
            font-size: 16px;
            background: #4ECDC4;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        button:hover {
            background: #45B7D1;
            transform: scale(1.05);
        }
        
        .btn-clear {
            background: #ff6b6b;
        }
        
        .btn-clear:hover {
            background: #ff5252;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-size: 16px;
            text-transform: uppercase;
        }
        
        td {
            padding: 12px 15px;
            border-bottom: 1px solid #ddd;
        }
        
        tr:hover {
            background: #f5f5f5;
            transition: background 0.3s;
        }
        
        tr:nth-child(even) {
            background: #fafafa;
        }
        
        .stats {
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
        }
        
        .stat-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            flex: 1;
            margin: 0 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .stat-number {
            font-size: 36px;
            font-weight: bold;
        }
        
        .stat-label {
            font-size: 14px;
            text-transform: uppercase;
        }
        
        .nav {
            text-align: center;
            margin-bottom: 20px;
        }
        
        .nav a {
            padding: 10px 20px;
            background: #45B7D1;
            color: white;
            text-decoration: none;
            margin: 0 5px;
            border-radius: 5px;
            display: inline-block;
            transition: all 0.3s;
        }
        
        .nav a:hover {
            background: #4ECDC4;
            transform: translateY(-2px);
        }
        
        .badge {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 12px;
            font-weight: bold;
            color: white;
        }
        
        .badge-high { background: #4CAF50; }
        .badge-medium { background: #FF9800; }
        .badge-low { background: #F44336; }
        
        .message {
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
            font-weight: bold;
            text-align: center;
        }
        
        .message-success {
            background: #4CAF50;
            color: white;
        }
        
        .message-error {
            background: #F44336;
            color: white;
        }
        
        .create-form {
            background: #f0f8ff;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 5px;
            border: 2px solid #45B7D1;
        }
        
        .create-form h3 {
            margin-top: 0;
            color: #45B7D1;
        }
        
        .form-row {
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
        }
        
        .form-row input, .form-row select {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        
        .btn-create {
            background: #4CAF50;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
        }
        
        .btn-create:hover {
            background: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="warning">
            ⚠️ ANTI-PATTERN EXAMPLE - THIS IS INTENTIONALLY BAD CODE ⚠️
        </div>
        
        <h1>📚 Student Data Management</h1>
        
        <div class="nav">
            <a href="/">🏠 Home</a>
            <a href="/grades">📊 View Grades</a>
        </div>"""
    
    # ANTI-PATTERN: Generating message HTML in Python
    if message:
        html += f"""
        <div class="message message-{message_type}">
            {message}
        </div>"""
    
    html += """
        
        <!-- ANTI-PATTERN: Create form mixed with display logic -->
        <div class="create-form">
            <h3>➕ Add New Student</h3>
            <form method="POST" action="/students">
                <div class="form-row">
                    <input type="text" name="name" placeholder="Full Name *" required>
                    <input type="email" name="email" placeholder="Email *" required>
                </div>
                <div class="form-row">
                    <input type="number" name="age" placeholder="Age" min="16" max="100">
                    <input type="text" name="major" placeholder="Major" list="major-list">
                    <datalist id="major-list">"""
    
    # ANTI-PATTERN: Building datalist options in Python
    for major in majors:
        html += f"""
                        <option value="{major[0]}">"""
    
    html += """
                    </datalist>
                    <input type="number" name="gpa" placeholder="GPA" step="0.01" min="0" max="4.0">
                </div>
                <button type="submit" class="btn-create">✅ Create Student</button>
            </form>
        </div>
        
        <div class="stats">
            <div class="stat-box">
                <div class="stat-number" id="totalStudents">""" + str(len(students)) + """</div>
                <div class="stat-label">Total Students</div>
            </div>
            <div class="stat-box">
                <div class="stat-number" id="avgGPA">""" + str(round(sum(s[5] for s in students) / len(students) if students else 0, 2)) + """</div>
                <div class="stat-label">Average GPA</div>
            </div>
            <div class="stat-box">
                <div class="stat-number" id="majors">""" + str(len(majors)) + """</div>
                <div class="stat-label">Majors</div>
            </div>
        </div>
        
        <div class="controls">
            <form method="GET" action="/students" style="display: inline-block;">
                <input type="text" name="search" placeholder="Search by name..." value\"""" + search + """">
                <button type="submit">🔍 Search</button>
            </form>
            
            <form method="GET" action="/students" style="display: inline-block;">
                <select name="major" onchange="this.form.submit()">
                    <option value="">All Majors</option>
"""
    
    # ANTI-PATTERN: Building HTML in loops in Python
    for major in majors:
        selected = "selected" if major[0] == filter_major else ""
        html += f'                    <option value="{major[0]}" {selected}>{major[0]}</option>\n'
    
    html += """
                </select>
            </form>
            
            <button class="btn-clear" onclick="window.location.href='/students'">❌ Clear Filters</button>
            
            <button onclick="downloadCSV()">💾 Download CSV</button>
            <button onclick="printTable()">🖨️ Print</button>
        </div>
        
        <table id="studentTable">
            <thead>
                <tr>
                    <th onclick="sortTable(0)">ID 🔽</th>
                    <th onclick="sortTable(1)">Name 🔽</th>
                    <th onclick="sortTable(2)">Email 🔽</th>
                    <th onclick="sortTable(3)">Age 🔽</th>
                    <th onclick="sortTable(4)">Major 🔽</th>
                    <th onclick="sortTable(5)">GPA 🔽</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
"""
    
    # ANTI-PATTERN: More HTML generation in Python loops
    if not students:
        html += """
                <tr>
                    <td colspan="7" style="text-align: center; padding: 50px; color: #999;">
                        No students found 😢
                    </td>
                </tr>
"""
    else:
        for student in students:
            gpa_class = "badge-high" if student[5] >= 3.5 else ("badge-medium" if student[5] >= 3.0 else "badge-low")
            html += f"""
                <tr onclick="showDetails({student[0]})" style="cursor: pointer;">
                    <td>{student[0]}</td>
                    <td><strong>{student[1]}</strong></td>
                    <td>{student[2]}</td>
                    <td>{student[3]}</td>
                    <td>{student[4]}</td>
                    <td><span class="badge {gpa_class}">{student[5]}</span></td>
                    <td>
                        <button onclick="event.stopPropagation(); editStudent({student[0]})">✏️ Edit</button>
                        <button onclick="event.stopPropagation(); deleteStudent({student[0]})" class="btn-clear">🗑️ Delete</button>
                    </td>
                </tr>
"""
    
    html += """
            </tbody>
        </table>
    </div>
    
    <!-- ANTI-PATTERN: Inline JavaScript instead of separate file -->
    <script>
        // ANTI-PATTERN: Global variables everywhere
        var currentSort = -1;
        var ascending = true;
        var students = [
"""
    
    # ANTI-PATTERN: Embedding data in JavaScript
    for i, student in enumerate(students):
        # ANTI-PATTERN: No proper escaping for special characters
        name = str(student[1]).replace("'", "\\'").replace('"', '\\"')
        email = str(student[2]).replace("'", "\\'").replace('"', '\\"')
        major = str(student[4]).replace("'", "\\'").replace('"', '\\"')
        html += f"            {{'id': {student[0]}, 'name': '{name}', 'email': '{email}', 'age': {student[3]}, 'major': '{major}', 'gpa': {student[5]}}}"
        if i < len(students) - 1:
            html += ",\n"
        else:
            html += "\n"
    
    html += """
        ];
        
        // ANTI-PATTERN: Huge function doing everything
        function sortTable(columnIndex) {
            var table = document.getElementById("studentTable");
            var rows = Array.from(table.rows).slice(1);
            
            if (currentSort === columnIndex) {
                ascending = !ascending;
            } else {
                ascending = true;
                currentSort = columnIndex;
            }
            
            rows.sort(function(a, b) {
                var aValue = a.cells[columnIndex].textContent.trim();
                var bValue = b.cells[columnIndex].textContent.trim();
                
                // Try to parse as number
                var aNum = parseFloat(aValue);
                var bNum = parseFloat(bValue);
                
                if (!isNaN(aNum) && !isNaN(bNum)) {
                    return ascending ? aNum - bNum : bNum - aNum;
                }
                
                return ascending ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
            });
            
            var tbody = table.querySelector('tbody');
            tbody.innerHTML = '';
            rows.forEach(function(row) {
                tbody.appendChild(row);
            });
            
            // Update header arrows
            var headers = table.querySelectorAll('th');
            headers.forEach(function(header, index) {
                if (index === columnIndex) {
                    var text = header.textContent.replace(' 🔽', '').replace(' 🔼', '');
                    header.textContent = text + (ascending ? ' 🔼' : ' 🔽');
                } else {
                    header.textContent = header.textContent.replace(' 🔽', '').replace(' 🔼', '') + ' 🔽';
                }
            });
        }
        
        // ANTI-PATTERN: Alert instead of proper UI
        function showDetails(studentId) {
            var student = students.find(function(s) { return s.id === studentId; });
            if (student) {
                var message = "Student Details:\\n\\n";
                message += "ID: " + student.id + "\\n";
                message += "Name: " + student.name + "\\n";
                message += "Email: " + student.email + "\\n";
                message += "Age: " + student.age + "\\n";
                message += "Major: " + student.major + "\\n";
                message += "GPA: " + student.gpa + "\\n";
                alert(message);
            }
        }
        
        function editStudent(studentId) {
            // ANTI-PATTERN: Using prompt for data entry
            var student = students.find(function(s) { return s.id === studentId; });
            if (student) {
                var newName = prompt("Enter new name:", student.name);
                if (newName) {
                    alert("Edit functionality not implemented! This is a demo.");
                    console.log("Would edit student " + studentId + " with name: " + newName);
                }
            }
        }
        
        function deleteStudent(studentId) {
            // ANTI-PATTERN: No confirmation, poor error handling
            var student = students.find(function(s) { return s.id === studentId; });
            if (student && confirm("Are you sure you want to delete " + student.name + "? This will also delete all their grades!")) {
                // ANTI-PATTERN: Creating and submitting form via JavaScript
                var form = document.createElement('form');
                form.method = 'POST';
                form.action = '/students';
                
                var actionInput = document.createElement('input');
                actionInput.type = 'hidden';
                actionInput.name = 'action';
                actionInput.value = 'delete';
                form.appendChild(actionInput);
                
                var idInput = document.createElement('input');
                idInput.type = 'hidden';
                idInput.name = 'delete_id';
                idInput.value = studentId;
                form.appendChild(idInput);
                
                document.body.appendChild(form);
                form.submit();
            }
        }
        
        function downloadCSV() {
            // ANTI-PATTERN: Client-side CSV generation with poor formatting
            var csv = "ID,Name,Email,Age,Major,GPA\\n";
            students.forEach(function(student) {
                csv += student.id + ",";
                csv += student.name + ",";
                csv += student.email + ",";
                csv += student.age + ",";
                csv += student.major + ",";
                csv += student.gpa + "\\n";
            });
            
            var blob = new Blob([csv], { type: 'text/csv' });
            var url = window.URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = 'students.csv';
            a.click();
        }
        
        function printTable() {
            window.print();
        }
        
        // ANTI-PATTERN: Code runs on page load without proper initialization
        console.log("Page loaded with " + students.length + " students");
        
        // ANTI-PATTERN: Manipulating DOM before it's ready
        setTimeout(function() {
            var rows = document.querySelectorAll('tbody tr');
            rows.forEach(function(row, index) {
                setTimeout(function() {
                    row.style.animation = 'fadeIn 0.5s';
                }, index * 50);
            });
        }, 100);
        
         // ANTI-PATTERN: Global error handler that just logs
        window.onerror = function(msg, url, lineNo, columnNo, error) {
            console.log("Error: " + msg);
            return false;
        };
        
        // ANTI-PATTERN: Inline event handlers
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'f') {
                e.preventDefault();
                document.querySelector('input[name="search"]').focus();
            }
        });
        
        // ANTI-PATTERN: Polling instead of event-driven
        setInterval(function() {
            var totalStudents = document.getElementById('totalStudents');
            if (totalStudents) {
                totalStudents.style.transform = 'scale(1.1)';
                setTimeout(function() {
                    totalStudents.style.transform = 'scale(1)';
                }, 200);
            }
        }, 5000);
    </script>
    
    <style>
        /* ANTI-PATTERN: More styles at the end of the document */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @media print {
            .controls, .nav, button { display: none; }
        }
    </style>
</body>
</html>
"""
    
    return html

