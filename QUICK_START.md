# 🚀 Quick Start Guide

## Get Up and Running in 2 Minutes

---

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

---

## Installation & Running

### Option 1: Automated Start Script (Recommended)

#### On macOS/Linux:

```bash
./start.sh
```

#### On Windows:

```cmd
start.bat
```

### Option 2: Manual Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python3 terrible_server.py
```

### Option 3: One-Liner

```bash
pip install Flask==3.0.0 && python3 terrible_server.py
```

---

## Access the Application

Once running, open your browser to:

```
http://localhost:5000
```

### Available Pages:

- **Home**: `http://localhost:5000/`
- **Students**: `http://localhost:5000/students`
- **Grades**: `http://localhost:5000/grades`

---

## Stop the Server

Press `Ctrl + C` in the terminal

---

## Project Files Overview

| File | Purpose |
|------|---------|
| `README.md` | Full project documentation |
| `QUICK_START.md` | This file - fast setup guide |
| `ANTI_PATTERNS_CHEAT_SHEET.md` | Complete list of all anti-patterns |
| `GOOD_VS_BAD.md` | Side-by-side code comparisons |
| `terrible_server.py` | Main Flask server (intentionally bad) |
| `student_page.py` | Student data page (huge file, mixed technologies) |
| `grades_page.py` | Grades page (huge file, mixed technologies) |
| `requirements.txt` | Python dependencies |
| `start.sh` | Automated start script (Unix) |
| `start.bat` | Automated start script (Windows) |

---

## Quick Demonstration Flow

### For Instructors (30-minute session):

1. **Setup (5 min)**
   - Clone/download project
   - Run `./start.sh`
   - Show it running

2. **Show the Bad Code (15 min)**
   - Open `student_page.py` in editor
   - Point out mixed HTML/CSS/JS/SQL/Python
   - Demonstrate inline styles and scripts
   - Show lack of separation of concerns

3. **Show How to Fix (5 min)**
   - Open `GOOD_VS_BAD.md`
   - Show ORM example
   - Explain proper architecture

4. **Discussion & Q&A**
   - Why these patterns are bad
   - Real-world consequences
   - Questions from students

---

## Sample Data Included

The database comes pre-populated with:

- **10 fictional students**
  - Names: Alice Johnson, Bob Smith, Charlie Brown, etc.
  - Majors: Computer Science, Mathematics, Physics, etc.
  - GPAs ranging from 3.1 to 3.9

- **21 grade records**
  - Various courses
  - Grades from A to C+
  - Different semesters
  - Credit hours

---

## Common Issues & Solutions

### Issue: "Flask not found"
```bash
pip install Flask==3.0.0
```

### Issue: "Port 5000 already in use"
Edit `terrible_server.py`, change line:
```python
app.run(debug=True, port=5000)  # Change 5000 to another port like 5001
```

### Issue: Database not created
Delete `students.db` if it exists and restart the server. It will be recreated automatically.

### Issue: Permission denied on start.sh
```bash
chmod +x start.sh
```

---

## Learning Path for Students

### Beginner Level:

1. Read `README.md` to understand the project
2. Run the application and explore both pages
3. Read `ANTI_PATTERNS_CHEAT_SHEET.md`
4. Identify 5 anti-patterns in the code

### Intermediate Level:

5. Read `GOOD_VS_BAD.md` for proper solutions
6. Pick one page and plan how you'd refactor it
7. Write a code review document

### Advanced Level:

9. Fully refactor one page following best practices
10. Implement an ORM (SQLAlchemy)
11. Separate HTML into Jinja2 templates
12. Add proper error handling and tests
13. Create a secure API endpoint

---

## Assignment Ideas

### Quick (1 hour):
- List 10 anti-patterns with line numbers
- Explain why inline CSS is bad
- Document separation of concerns violations

### Medium (3-4 hours):
- Refactor the student page properly
- Create separate CSS and JS files
- Use an ORM for database queries

### Comprehensive (1-2 weeks):
- Complete application refactor
- Implement proper MVC architecture
- Add authentication system
- Write comprehensive tests

---

## Testing Checklist

- [ ] Server starts without errors
- [ ] Home page loads correctly
- [ ] Students page shows 10 students
- [ ] Grades page shows 21 grade records
- [ ] Search functionality works
- [ ] Filter by major works
- [ ] Sorting tables works
- [ ] Statistics display correctly
- [ ] No Python errors in console

---

## What Makes This Example Valuable

This code demonstrates:

✅ **Real-world mistakes** developers actually make
✅ **Architecture problems** that hurt maintainability
✅ **Technical debt** that accumulates in projects
✅ **The importance** of following best practices

By seeing BAD code, students learn to:
- Recognize anti-patterns
- Understand WHY certain practices are bad
- Appreciate good architecture
- Write better code
- Think critically about code quality

---

## Next Steps

After exploring this anti-pattern example:

1. **Study the good alternatives** in `GOOD_VS_BAD.md`
2. **Practice good coding** with proper frameworks
3. **Build projects** using best practices
4. **Review code** with a critical eye

---

## Additional Resources

- Flask documentation: https://flask.palletsprojects.com/
- SQLAlchemy ORM: https://www.sqlalchemy.org/
- Python PEP 8: https://peps.python.org/pep-0008/

---

## Need Help?

If you encounter issues:

1. Check `README.md` for detailed information
2. Review the anti-pattern documentation
3. Verify Python and Flask are installed correctly
4. Check that port 5000 is available

---

## Remember

> "This code is intentionally bad for educational purposes.
> Learn from these mistakes, but never replicate them in real projects!"

---

**Happy Learning! 🎓**

*Understanding what NOT to do is just as important as knowing what TO do.*

