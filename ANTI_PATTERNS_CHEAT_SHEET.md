# 🚫 Anti-Patterns Cheat Sheet

## Quick Reference Guide for Instructors and Students

This document catalogs all the intentional anti-patterns present in this codebase.

---

## 🔴 CRITICAL SECURITY ISSUES

### 1. SQL Injection Vulnerabilities
**Location**: `student_page.py` lines ~20-30, `grades_page.py` lines ~20-40

**Bad Code**:
```python
query = "SELECT * FROM students WHERE name LIKE '%" + search + "%'"
c.execute(query)
```

**Why It's Bad**:
- Direct string concatenation with user input
- Attacker can inject SQL code
- Can lead to data theft, data loss, or complete database compromise

**Attack Example**:
```
search = "'; DROP TABLE students; --"
```

**Correct Approach**:
```python
query = "SELECT * FROM students WHERE name LIKE ?"
c.execute(query, (f"%{search}%",))
```

---

### 2. No Input Validation
**Location**: Throughout `student_page.py` and `grades_page.py`

**Why It's Bad**:
- No checking of user input
- No sanitization
- No type checking
- XSS vulnerabilities possible

**Correct Approach**:
- Use validation libraries (WTForms, Pydantic)
- Sanitize all user input
- Implement proper error handling

---

## 🏗️ ARCHITECTURE ANTI-PATTERNS

### 3. No Separation of Concerns
**Location**: All files

**Bad Practices**:
- HTML, CSS, JavaScript, SQL, and Python all in the same file
- Business logic mixed with presentation layer
- No MVC or similar pattern

**What Should Be Done**:
```
project/
├── models/          # Database models
├── views/           # Route handlers
├── templates/       # HTML templates
├── static/
│   ├── css/        # Stylesheets
│   └── js/         # JavaScript files
└── utils/          # Helper functions
```

---

### 4. Inline CSS and JavaScript
**Location**: `student_page.py` and `grades_page.py`

**Why It's Bad**:
- No code reuse
- Difficult to maintain
- No caching benefits
- Violates separation of concerns
- Makes files enormous

**Correct Approach**:
- Separate CSS files in `static/css/`
- Separate JavaScript files in `static/js/`
- Use a templating engine like Jinja2

---

### 5. HTML Generation in Python
**Location**: Both page files, throughout

**Bad Code**:
```python
html = "<div>" + some_value + "</div>"
```

**Why It's Bad**:
- Hard to read and maintain
- No syntax highlighting
- Prone to errors
- Security risks (XSS)

**Correct Approach**:
- Use templating engines (Jinja2, Django templates)
- Keep HTML in `.html` files
- Use template inheritance

---

## 💾 DATABASE ANTI-PATTERNS

### 6. No Connection Pooling
**Location**: `student_page.py` and `grades_page.py`

**Bad Code**:
```python
def render_page():
    conn = sqlite3.connect("students.db")
    # ... use connection
    conn.close()
```

**Why It's Bad**:
- Creates new connection for every request
- Poor performance
- Resource waste
- Can exhaust database connections

**Correct Approach**:
- Use SQLAlchemy with connection pooling
- Implement context managers
- Reuse connections

---

### 7. Hardcoded Database Path
**Location**: `terrible_server.py` line 12

**Bad Code**:
```python
db_path = "students.db"
```

**Why It's Bad**:
- Not configurable
- Different paths needed for dev/test/prod
- Can't use environment variables

**Correct Approach**:
```python
import os
DB_PATH = os.environ.get('DATABASE_URL', 'students.db')
```

---

### 8. No ORM Usage
**Location**: All database interactions

**Why It's Bad**:
- Writing raw SQL queries
- No database abstraction
- Difficult to switch databases
- More prone to errors

**Correct Approach**:
- Use SQLAlchemy or Django ORM
- Define models as classes
- Let ORM handle SQL generation

---

## 🎨 CODE ORGANIZATION ISSUES

### 9. Giant Functions
**Location**: Both page files

**Why It's Bad**:
- Functions do too much
- Hard to test
- Difficult to maintain
- Violations of Single Responsibility Principle

**Correct Approach**:
- Break into smaller functions
- Each function should do one thing
- Maximum 20-30 lines per function

---

### 10. Repetitive Code (DRY Violation)
**Location**: Throughout

**Examples**:
- Similar HTML generation patterns repeated
- Duplicate styling code
- Repeated database connection logic

**Correct Approach**:
- Create reusable components
- Use template inheritance
- Create utility functions

---

### 11. No Error Handling
**Location**: All files

**Bad Code**:
```python
c.execute(query)  # No try-except
```

**Why It's Bad**:
- Application crashes on errors
- No user-friendly error messages
- Difficult to debug

**Correct Approach**:
```python
try:
    c.execute(query)
except sqlite3.Error as e:
    logger.error(f"Database error: {e}")
    return render_template('error.html', message="Database error")
```

---

## 🎭 FRONTEND ANTI-PATTERNS

### 12. Alert/Prompt for User Interaction
**Location**: JavaScript sections in both files

**Bad Code**:
```javascript
function editStudent(id) {
    var newName = prompt("Enter new name:");
    // ...
}
```

**Why It's Bad**:
- Poor user experience
- Blocking UI
- Not customizable
- Looks unprofessional

**Correct Approach**:
- Use modals or forms
- Implement proper UI components
- Use modern UI libraries

---

### 13. Global Variables
**Location**: JavaScript sections

**Bad Code**:
```javascript
var currentSort = -1;
var ascending = true;
var students = [...];
```

**Why It's Bad**:
- Namespace pollution
- Name collisions possible
- Difficult to track state
- Testing difficulties

**Correct Approach**:
```javascript
const StudentApp = {
    state: {
        currentSort: -1,
        ascending: true,
        students: [...]
    }
};
```

---

### 14. Inline Event Handlers
**Location**: HTML sections in both files

**Bad Code**:
```html
<button onclick="deleteStudent(1)">Delete</button>
```

**Why It's Bad**:
- Mixing JavaScript with HTML
- Hard to maintain
- CSP (Content Security Policy) violations

**Correct Approach**:
```javascript
document.getElementById('deleteBtn').addEventListener('click', handleDelete);
```

---

### 15. No Build Process
**Location**: Project structure

**Why It's Bad**:
- No minification
- No bundling
- No transpilation
- Poor performance

**Correct Approach**:
- Use webpack, Rollup, or Vite
- Minify and bundle assets
- Use a proper frontend framework

---

## 🐛 GENERAL BAD PRACTICES

### 16. Debug Mode in Production
**Location**: `terrible_server.py` last line

**Bad Code**:
```python
app.run(debug=True, port=5000)
```

**Why It's Bad**:
- Exposes sensitive information
- Shows detailed error messages to users
- Security risk
- Performance impact

**Correct Approach**:
```python
app.run(debug=os.environ.get('DEBUG', False), port=5000)
```

---

### 17. No Configuration Management
**Location**: Entire project

**Why It's Bad**:
- Hardcoded values everywhere
- No environment-specific configs
- Can't change settings without code changes

**Correct Approach**:
- Use configuration files
- Environment variables
- Config classes for different environments

---

### 18. No Logging
**Location**: All files

**Why It's Bad**:
- Console.log instead of proper logging
- No log levels
- Difficult to debug production issues
- No audit trail

**Correct Approach**:
```python
import logging
logger = logging.getLogger(__name__)
logger.error("Something went wrong")
```

---

### 19. No Tests
**Location**: Entire project

**Why It's Bad**:
- No way to verify functionality
- Refactoring is risky
- Bugs can slip through
- No regression testing

**Correct Approach**:
- Write unit tests
- Integration tests
- Use pytest or unittest

---

### 20. No API Design
**Location**: Route structure

**Why It's Bad**:
- Returns full HTML pages
- Not RESTful
- Can't be used by other clients
- Tight coupling

**Correct Approach**:
- Design RESTful API
- Return JSON
- Separate frontend and backend
- Use proper HTTP methods

---

## 📊 PERFORMANCE ISSUES

### 21. N+1 Query Problem
**Location**: Potential in both page files

**Why It's Bad**:
- Multiple queries when one would suffice
- Poor database performance
- Scalability issues

---

### 22. Client-Side Processing
**Location**: JavaScript statistics calculations

**Bad Practice**:
- Calculating statistics in JavaScript
- Should be done server-side or in database

---

### 23. No Caching
**Location**: Entire application

**Why It's Bad**:
- Same data fetched repeatedly
- Poor performance
- Unnecessary database load

---

## 🎯 TEACHING EXERCISES

### For Students:

1. **Find the SQL injection vulnerability** - Can you craft a malicious input?
2. **Refactor one page** - Choose either students or grades and restructure properly
3. **Security audit** - List all security issues you can find
4. **Performance analysis** - Identify bottlenecks
5. **Code review** - Write a detailed code review
6. **Architecture design** - Draw how this should be structured
7. **Create proper tests** - Write tests for core functionality
8. **Extract CSS** - Move all CSS to external files
9. **Implement an ORM** - Replace raw SQL with SQLAlchemy
10. **Add validation** - Implement proper input validation

---

## ✅ QUICK FIX CHECKLIST

To fix this codebase, you would need to:

- [ ] Use SQLAlchemy ORM
- [ ] Implement parameterized queries
- [ ] Separate HTML into Jinja2 templates
- [ ] Move CSS to external files
- [ ] Move JavaScript to external files
- [ ] Add input validation
- [ ] Implement error handling
- [ ] Add logging
- [ ] Use environment variables
- [ ] Create proper project structure
- [ ] Add unit tests
- [ ] Implement connection pooling
- [ ] Add authentication
- [ ] Implement CSRF protection
- [ ] Use blueprints for routing
- [ ] Add API endpoints
- [ ] Implement caching
- [ ] Add rate limiting
- [ ] Use proper configuration management
- [ ] Add documentation

---

## 📚 Recommended Reading

- OWASP Top 10 Security Risks
- Python PEP 8 Style Guide
- Flask Best Practices
- SQLAlchemy Documentation
- Clean Code by Robert C. Martin
- The Pragmatic Programmer

---

**Remember**: Every "bad" thing in this code is intentional for teaching purposes. In real projects, follow industry best practices and security guidelines!

