# 🔄 Good vs Bad Code Examples

## Side-by-Side Comparison Guide

This document shows what's wrong with the anti-pattern code and how it should be written instead.

---

## 1️⃣ Database Queries

### ❌ BAD (Current Code)

```python
# student_page.py
def render_student_page():
    search = request.args.get('search', '')
    
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    
    # SQL INJECTION VULNERABILITY!
    query = "SELECT * FROM students WHERE name LIKE '%" + search + "%'"
    c.execute(query)
    students = c.fetchall()
    
    conn.close()
```

**Problems**:
- SQL injection vulnerability
- No connection pooling
- Raw SQL queries
- No error handling
- Tuple results instead of named attributes

---

### ✅ GOOD (How it should be)

```python
# models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    age = db.Column(db.Integer)
    major = db.Column(db.String(100))
    gpa = db.Column(db.Float)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'age': self.age,
            'major': self.major,
            'gpa': self.gpa
        }

# views/students.py
from flask import Blueprint, request, render_template
from models import Student, db
import logging

logger = logging.getLogger(__name__)
students_bp = Blueprint('students', __name__)

@students_bp.route('/students')
def list_students():
    try:
        search = request.args.get('search', '').strip()
        
        query = Student.query
        
        if search:
            # Safe parameterized query via ORM
            query = query.filter(
                Student.name.ilike(f'%{search}%')
            )
        
        students = query.all()
        
        return render_template(
            'students/list.html',
            students=students,
            search=search
        )
    except Exception as e:
        logger.error(f"Error fetching students: {e}")
        return render_template('error.html', message="Error loading students"), 500
```

**Benefits**:
- No SQL injection possible
- Connection pooling handled by SQLAlchemy
- ORM provides cleaner code
- Proper error handling
- Named attributes instead of tuples
- Separation of concerns

---

## 2️⃣ HTML Generation

### ❌ BAD (Current Code)

```python
# student_page.py
def render_student_page():
    # ... database code ...
    
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>Students</title>
    <style>
        body { font-family: Arial; }
        .student { padding: 10px; }
    </style>
</head>
<body>
    <h1>Students</h1>
"""
    
    for student in students:
        html += f"""
    <div class="student">
        <h2>{student[1]}</h2>
        <p>Email: {student[2]}</p>
    </div>
"""
    
    html += """
</body>
</html>
"""
    
    return html
```

**Problems**:
- HTML in Python code
- Inline CSS
- No template reuse
- XSS vulnerabilities
- Difficult to maintain
- No auto-escaping

---

### ✅ GOOD (How it should be)

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Student Management{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <nav>
        <a href="{{ url_for('home') }}">Home</a>
        <a href="{{ url_for('students.list_students') }}">Students</a>
        <a href="{{ url_for('grades.list_grades') }}">Grades</a>
    </nav>
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>
```

```html
<!-- templates/students/list.html -->
{% extends "base.html" %}

{% block title %}Students - {{ super() }}{% endblock %}

{% block content %}
<div class="container">
    <h1>Students</h1>
    
    <form method="GET" action="{{ url_for('students.list_students') }}">
        <input type="text" 
               name="search" 
               value="{{ search }}" 
               placeholder="Search students...">
        <button type="submit">Search</button>
    </form>
    
    <div class="students-grid">
        {% for student in students %}
        <div class="student-card">
            <h2>{{ student.name }}</h2>
            <p>{{ student.email }}</p>
            <p>GPA: {{ student.gpa }}</p>
        </div>
        {% else %}
        <p>No students found.</p>
        {% endfor %}
    </div>
</div>
{% endblock %}
```

```css
/* static/css/style.css */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.students-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
}

.student-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 20px;
}
```

**Benefits**:
- Clean separation of concerns
- Reusable templates
- Auto-escaping prevents XSS
- Easy to maintain
- CSS in separate file
- Template inheritance
- Professional code structure

---

## 3️⃣ JavaScript Code

### ❌ BAD (Current Code)

```html
<!-- Inline in student_page.py -->
<script>
    // Global variables
    var students = [/* huge array embedded in HTML */];
    var currentSort = -1;
    
    function sortTable(col) {
        // 50 lines of sorting code
        var table = document.getElementById("studentTable");
        // ... massive function ...
    }
    
    function editStudent(id) {
        var newName = prompt("Enter new name:");
        alert("Not implemented!");
    }
</script>
```

**Problems**:
- Inline JavaScript
- Global variables
- No modules
- Alert/prompt for UI
- Data embedded in HTML
- No code reuse

---

### ✅ GOOD (How it should be)

```javascript
// static/js/students.js
class StudentManager {
    constructor() {
        this.students = [];
        this.currentSort = null;
        this.sortDirection = 'asc';
        this.init();
    }
    
    init() {
        this.fetchStudents();
        this.attachEventListeners();
    }
    
    async fetchStudents() {
        try {
            const response = await fetch('/api/students');
            if (!response.ok) throw new Error('Failed to fetch');
            this.students = await response.json();
            this.renderStudents();
        } catch (error) {
            console.error('Error fetching students:', error);
            this.showError('Failed to load students');
        }
    }
    
    attachEventListeners() {
        document.querySelectorAll('.sort-header').forEach(header => {
            header.addEventListener('click', (e) => {
                this.sortBy(e.target.dataset.column);
            });
        });
    }
    
    sortBy(column) {
        if (this.currentSort === column) {
            this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            this.currentSort = column;
            this.sortDirection = 'asc';
        }
        
        this.students.sort((a, b) => {
            const aVal = a[column];
            const bVal = b[column];
            const modifier = this.sortDirection === 'asc' ? 1 : -1;
            return aVal > bVal ? modifier : -modifier;
        });
        
        this.renderStudents();
    }
    
    renderStudents() {
        // Render using template or framework
    }
    
    showError(message) {
        // Show error in UI, not alert
        const errorDiv = document.getElementById('error-message');
        errorDiv.textContent = message;
        errorDiv.classList.add('visible');
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new StudentManager();
});
```

**Benefits**:
- Proper class structure
- No global variables
- Async/await for API calls
- Modular code
- Proper error handling
- Reusable components
- Modern JavaScript features

---

## 4️⃣ Project Structure

### ❌ BAD (Current Structure)

```
python-antipattern-example/
├── terrible_server.py       # 100 lines
├── student_page.py          # 500+ lines of mixed code
├── grades_page.py           # 500+ lines of mixed code
└── students.db
```

**Problems**:
- Only 3-4 files
- Everything mixed together
- No organization
- Impossible to test
- No scalability

---

### ✅ GOOD (How it should be)

```
student-management-system/
├── app/
│   ├── __init__.py          # App factory
│   ├── models/
│   │   ├── __init__.py
│   │   ├── student.py       # Student model
│   │   └── grade.py         # Grade model
│   ├── views/
│   │   ├── __init__.py
│   │   ├── students.py      # Student routes
│   │   ├── grades.py        # Grade routes
│   │   └── api.py           # API endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── student_service.py
│   │   └── grade_service.py
│   ├── forms/
│   │   ├── __init__.py
│   │   └── student_forms.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── students/
│   │   │   ├── list.html
│   │   │   ├── detail.html
│   │   │   └── edit.html
│   │   └── grades/
│   │       ├── list.html
│   │       └── detail.html
│   └── static/
│       ├── css/
│       │   ├── style.css
│       │   └── students.css
│       ├── js/
│       │   ├── main.js
│       │   └── students.js
│       └── images/
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   └── test_services.py
├── migrations/              # Database migrations
├── config.py               # Configuration
├── requirements.txt
├── .env.example
├── .gitignore
└── run.py                  # Application entry point
```

**Benefits**:
- Clear separation of concerns
- Easy to navigate
- Testable components
- Scalable structure
- Industry standard
- Team-friendly

---

## 5️⃣ Configuration

### ❌ BAD (Current Code)

```python
# terrible_server.py
db_path = "students.db"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**Problems**:
- Hardcoded values
- No environment support
- Debug mode always on
- Not configurable

---

### ✅ GOOD (How it should be)

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///dev_students.db'
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_students.db'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
```

```python
# run.py
import os
from app import create_app

app = create_app(os.environ.get('FLASK_ENV') or 'development')

if __name__ == '__main__':
    app.run(
        host=os.environ.get('HOST', '0.0.0.0'),
        port=int(os.environ.get('PORT', 5000))
    )
```

```bash
# .env.example
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///students.db
DEBUG=True
```

**Benefits**:
- Environment-specific configs
- Secure secret management
- Easy to deploy
- Professional approach

---

## 6️⃣ Error Handling

### ❌ BAD (Current Code)

```python
def render_student_page():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute(query)  # No error handling!
    students = c.fetchall()
    conn.close()
    # If any error occurs, app crashes
```

**Problems**:
- No try-except blocks
- App crashes on errors
- No logging
- Poor user experience

---

### ✅ GOOD (How it should be)

```python
# views/students.py
import logging
from flask import Blueprint, render_template, flash
from sqlalchemy.exc import SQLAlchemyError
from models import Student

logger = logging.getLogger(__name__)
students_bp = Blueprint('students', __name__)

@students_bp.route('/students')
def list_students():
    try:
        students = Student.query.all()
        return render_template('students/list.html', students=students)
        
    except SQLAlchemyError as e:
        logger.error(f"Database error in list_students: {str(e)}", exc_info=True)
        flash('An error occurred while loading students', 'error')
        return render_template('error.html', 
                             message='Unable to load students'), 500
                             
    except Exception as e:
        logger.error(f"Unexpected error in list_students: {str(e)}", exc_info=True)
        flash('An unexpected error occurred', 'error')
        return render_template('error.html',
                             message='An unexpected error occurred'), 500

@students_bp.errorhandler(404)
def not_found(error):
    return render_template('error.html', message='Page not found'), 404

@students_bp.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}", exc_info=True)
    return render_template('error.html', 
                         message='Internal server error'), 500
```

**Benefits**:
- Graceful error handling
- Proper logging
- User-friendly messages
- App stays running
- Errors are tracked

---

## 7️⃣ Testing

### ❌ BAD (Current Code)

```
No tests exist!
```

**Problems**:
- Can't verify functionality
- Refactoring is risky
- Bugs slip through
- No confidence in code

---

### ✅ GOOD (How it should be)

```python
# tests/test_models.py
import pytest
from app import create_app, db
from app.models import Student

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_student_creation(app):
    """Test creating a new student"""
    with app.app_context():
        student = Student(
            name="John Doe",
            email="john@example.com",
            age=20,
            major="Computer Science",
            gpa=3.5
        )
        db.session.add(student)
        db.session.commit()
        
        assert student.id is not None
        assert student.name == "John Doe"

def test_student_query(app):
    """Test querying students"""
    with app.app_context():
        # Create test data
        student1 = Student(name="Alice", email="alice@test.com")
        student2 = Student(name="Bob", email="bob@test.com")
        db.session.add_all([student1, student2])
        db.session.commit()
        
        # Test query
        students = Student.query.all()
        assert len(students) == 2

def test_list_students_route(client):
    """Test the students list route"""
    response = client.get('/students')
    assert response.status_code == 200
    assert b'Students' in response.data
```

```python
# tests/test_views.py
def test_search_students(client, app):
    """Test student search functionality"""
    with app.app_context():
        # Create test student
        student = Student(name="Test User", email="test@test.com")
        db.session.add(student)
        db.session.commit()
    
    # Test search
    response = client.get('/students?search=Test')
    assert response.status_code == 200
    assert b'Test User' in response.data

def test_empty_search(client):
    """Test search with no results"""
    response = client.get('/students?search=NonexistentName')
    assert response.status_code == 200
    assert b'No students found' in response.data
```

**Benefits**:
- Confidence in code
- Catch bugs early
- Safe refactoring
- Documentation through tests
- Continuous integration ready

---

## 📊 Summary Table

| Aspect | Bad Approach | Good Approach |
|--------|-------------|---------------|
| **SQL Queries** | String concatenation | ORM with parameterized queries |
| **HTML** | Generated in Python | Jinja2 templates |
| **CSS** | Inline styles | External stylesheets |
| **JavaScript** | Inline scripts | External modules |
| **Structure** | 2-3 huge files | Organized MVC structure |
| **Config** | Hardcoded values | Environment variables |
| **Errors** | No handling | Try-except with logging |
| **Database** | Raw connections | Connection pooling |
| **Security** | SQL injection | Parameterized queries |
| **Testing** | None | Comprehensive tests |

---

## 🎯 Key Takeaways

1. **Always use an ORM** - Prevents SQL injection and provides cleaner code
2. **Separate concerns** - HTML, CSS, JS, and Python should be in different files
3. **Use templates** - Let the framework handle HTML generation
4. **Handle errors** - Always use try-except and log errors
5. **Write tests** - Tests save time and prevent bugs
6. **Use configuration** - Never hardcode values
7. **Follow conventions** - Use established project structures
8. **Think security first** - Validate input, use HTTPS, sanitize data

---

## 📚 Next Steps for Students

1. Pick one "bad" example above
2. Implement the "good" version
3. Compare the differences
4. Understand *why* the good version is better
5. Apply these principles to your own projects

**Remember**: Professional code is about more than just "working" - it's about maintainability, security, scalability, and teamwork!

