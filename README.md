# 🎬 MovieProduction — Actor Management System (DBMS + Python GUI)

> **Course / Lab**: Database Management Systems (DBMS) & Object-Oriented Programming (Python)  
> **Level**: 1st Year Engineering (B.Tech / B.E.)  
> **Architecture**: Two-Tier Architecture (Client-Server)  
> **Key Focus**: Viva Voce Preparation, CRUD Mechanics, & Practical Concepts  

---

## 📌 1. Project Overview

This project is a desktop-based Database Management System application built using **Python (Tkinter)** for the Graphical User Interface (GUI) and **MySQL** as the Relational Database Management System (RDBMS). 

It connects to a database named `MovieProduction` and performs full **CRUD** operations (Create, Read, Update, Delete) on the `ACTOR` entity with real-time UI synchronization, input validation, and transaction handling.

---

## 🏗️ 2. System Architecture: 2-Tier Architecture

In Indian engineering lab exams, examiners frequently ask about the system architecture. This project implements a **Two-Tier (Client-Server) Architecture**:

```
+------------------------------------+
|       TIER 1: PRESENTATION LAYER   |
|     (Python 3 + Tkinter / ttk)     |
|   - Form Entries (ID, Name, etc.)  |
|   - Event Handlers & Validation    |
|   - Listbox Display & Status Bar   |
+------------------------------------+
                  ▲
                  │  (TCP/IP Port 3306)
                  │  mysql-connector-python API
                  ▼
+------------------------------------+
|         TIER 2: DATA LAYER         |
|            (MySQL Server)          |
|   - Database: MovieProduction      |
|   - Table: ACTOR                   |
|   - ACID Engine: InnoDB            |
+------------------------------------+
```

1. **Client Tier (Presentation & Application Logic)**:
   - The user interacts with the Tkinter desktop GUI.
   - Performs client-side validation (ensures `Actor_ID` is an integer, `Fee` is numeric, required fields aren't empty).
2. **Database Tier (Storage & Integrity)**:
   - MySQL Server manages data persistence, enforces table constraints (Primary Key, NOT NULL), and ensures ACID properties via the InnoDB storage engine.
3. **Bridge / Driver (`mysql-connector-python`)**:
   - Translates Python database API calls (PEP 249) into native MySQL client/server network protocol packets over port 3306.

---

## 🛠️ 3. Technology Stack & Why We Used Them

| Component | Technology | Why We Used It (Viva Justification) |
| :--- | :--- | :--- |
| **Programming Language** | Python 3 | High readability, native support for GUI through standard libraries, and rich database API standard (PEP 249). |
| **GUI Framework** | Tkinter & `ttk` | Built-in with Python (no heavy external dependencies), cross-platform, light on memory, and event-driven. |
| **Database Server** | MySQL Community Server | Industry-standard open-source RDBMS supporting SQL standard, ACID transactions, and robust indexing. |
| **Database Driver** | `mysql-connector-python` | Official Oracle-supported driver for pure Python-MySQL communication. |
| **Database Engine** | InnoDB | Supports Foreign Keys, Crash Recovery, and ACID-compliant Transactions with Row-Level Locking. |

---

## 🗄️ 4. Database Schema & Design

### Database: `MovieProduction`
### Table: `ACTOR`

```sql
CREATE DATABASE IF NOT EXISTS MovieProduction;
USE MovieProduction;

CREATE TABLE IF NOT EXISTS ACTOR (
    Actor_ID INT PRIMARY KEY,
    ActorName VARCHAR(100),
    Gender VARCHAR(10),
    Nationality VARCHAR(50),
    Fee DECIMAL(10, 2)
);
```

### Attribute Analysis (Viva Points):
- **`Actor_ID INT PRIMARY KEY`**: 
  - **Candidate Key selected as Primary Key**.
  - Enforces **Entity Integrity Constraint**: Must be **UNIQUE** and **NOT NULL**. Prevents duplicate entries.
- **`ActorName VARCHAR(100)`**:
  - Variable-length character string. Unlike `CHAR(100)` which allocates 100 bytes fixed, `VARCHAR` only stores the actual characters + 1 byte prefix, saving memory.
- **`Gender VARCHAR(10)`**: Stores gender classification (e.g., `'Male'`, `'Female'`).
- **`Nationality VARCHAR(50)`**: Country of origin.
- **`Fee DECIMAL(10, 2)`**: 
  - **Fixed-point numeric type**: Exact precision for monetary values.
  - `10` is the **Precision** (total number of significant digits).
  - `2` is the **Scale** (number of digits after the decimal point).
  - *Why not `FLOAT` or `DOUBLE`?* Floating-point types introduce round-off errors due to binary representation; `DECIMAL` is mathematically exact.

---

## ⚙️ 5. How It Works (CRUD Mechanics)

### 1. Connection Life Cycle
Every operation creates a clean connection using `get_connection()`:
```python
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="MovieProduction"
)
```
- **Connection**: Creates an active socket channel with MySQL Server on port `3306`.
- **Cursor**: An operational pointer that executes queries and iterates over result sets.
- **Clean Close**: `cursor.close()` and `conn.close()` prevent database connection leaks and socket exhaustion.

---

### 2. Create (Insert Operation - DML)
```python
query = "INSERT INTO ACTOR (Actor_ID, ActorName, Gender, Nationality, Fee) VALUES (%s, %s, %s, %s, %s)"
cursor.execute(query, (actor_id, name, gender, nationality, fee))
conn.commit()
```
- **Parameterized Query (`%s`)**: Protects against **SQL Injection Attacks** by treating user input strictly as literal values rather than executable SQL code.
- **`conn.commit()`**: In MySQL InnoDB, auto-commit is disabled inside script transactions. You must explicitly call `commit()` to write changes permanently to disk.

---

### 3. Read (Select Operation - DQL)
```python
cursor.execute("SELECT Actor_ID, ActorName, Gender, Nationality, Fee FROM ACTOR ORDER BY Actor_ID ASC")
rows = cursor.fetchall()
```
- **`cursor.fetchall()`**: Pulls the entire query result set into a Python list of tuples.
- The UI loops over `rows` and formats them with fixed column widths inside the `tk.Listbox`.
- **Interactive selection**: Binding `<<ListboxSelect>>` reads the clicked index and auto-populates the input fields for fast updating.

---

### 4. Update (Modify Operation - DML)
```python
query = "UPDATE ACTOR SET ActorName=%s, Gender=%s, Nationality=%s, Fee=%s WHERE Actor_ID=%s"
cursor.execute(query, (name, gender, nationality, fee, actor_id))
conn.commit()
```
- Uses the `WHERE Actor_ID = %s` clause to identify the specific tuple.
- `cursor.rowcount` checks how many rows were updated; if `0`, it alerts that the ID does not exist.

---

### 5. Delete (Remove Operation - DML)
```python
cursor.execute("DELETE FROM ACTOR WHERE Actor_ID = %s", (actor_id,))
conn.commit()
```
- Prompts user confirmation via `messagebox.askyesno()` to prevent accidental data loss.
- Deletes the row matching the primary key and commits the transaction.

---

## 🧠 6. Viva Voce Cheat Sheet (Most Asked Questions & Model Answers)

Here are the exact questions external examiners love to ask 1st year engineering students:

### Q1: What is the difference between DDL, DML, and DQL? Which did you use?
> **Answer**:
> - **DDL (Data Definition Language)**: Defines schema and table structures (`CREATE DATABASE`, `CREATE TABLE`).
> - **DML (Data Manipulation Language)**: Modifies records (`INSERT`, `UPDATE`, `DELETE`).
> - **DQL (Data Query Language)**: Reads records (`SELECT`).
> In this project, we executed DDL to create `MovieProduction` and `ACTOR`, and our Python app executes DML and DQL for daily operations.

---

### Q2: Why is `conn.commit()` needed for INSERT/UPDATE/DELETE, but NOT for SELECT?
> **Answer**:
> DML commands modify the database state. Under transaction management, changes are initially held in memory (InnoDB redo/undo buffer). `conn.commit()` writes these changes permanently to disk. SELECT queries only read data without modifying state, so no commit is needed.

---

### Q3: Why did you use `%s` placeholders instead of Python f-strings like `f"INSERT INTO ACTOR VALUES ({id}, '{name}')"`?
> **Answer**:
> String concatenation or f-strings leave the application vulnerable to **SQL Injection Attacks** (where malicious input like `' OR '1'='1` can hijack or wipe the database). Using parameterized queries (`%s`) makes the database driver escape and treat user input strictly as data literals.

---

### Q4: What are ACID properties? How does this application satisfy them?
> **Answer**:
> - **Atomicity**: An operation either completely succeeds or completely fails (`commit` on success, rollback on error).
> - **Consistency**: Primary key and data type constraints ensure invalid data cannot corrupt the table.
> - **Isolation**: Concurrent database transactions do not interfere with each other (managed by InnoDB).
> - **Durability**: Once `conn.commit()` finishes, data is safely written to disk and survives power loss.

---

### Q5: What is a Primary Key? Can it accept NULL values?
> **Answer**:
> A Primary Key is a minimal superkey chosen to uniquely identify every tuple in a relation. It **cannot** accept `NULL` values according to the **Entity Integrity Rule**.

---

### Q6: What is the difference between `CHAR` and `VARCHAR`?
> **Answer**:
> `CHAR` is fixed-length (pads unused space with blanks). `VARCHAR` is variable-length (only uses storage equal to the actual character length plus length-prefix bytes), making `VARCHAR` much more space-efficient.

---

### Q7: What does `root.mainloop()` do in Tkinter?
> **Answer**:
> `mainloop()` is an infinite event-listening loop. It monitors user actions (mouse clicks, keystrokes, window resizing), processes events, triggers bound callback functions, and refreshes the GUI until the window is closed.

---

### Q8: What happens if you try to insert an existing `Actor_ID`?
> **Answer**:
> MySQL rejects the query with error code `1062 (Duplicate entry for key 'PRIMARY')`. The `try-except Error as err` block in Python catches `mysql.connector.Error` and shows a friendly error dialog (`messagebox.showerror`) instead of crashing the program.

---

### Q9: Why did you choose `DECIMAL(10, 2)` instead of `FLOAT` for Fee?
> **Answer**:
> `FLOAT` uses binary floating-point representation (IEEE 754), which causes rounding and approximation inaccuracies in currency. `DECIMAL` stores numbers as base-10 strings/integers, guaranteeing 100% exact precision up to 2 decimal places.

---

### Q10: What is a Database Cursor?
> **Answer**:
> A Cursor is a database control structure that acts as a pointer to the result set of a SQL query. It allows the Python program to fetch rows sequentially or in bulk (`fetchall()`) and execute queries one by one.

---

## 🚀 7. How to Run the Project

### Prerequisites:
1. **Python 3.10+** installed.
2. **MySQL Server** installed and running on port `3306`.
3. Install required connector:
   ```bash
   pip install mysql-connector-python
   ```

### Database Initialization:
Log in to MySQL and create the database and table:
```bash
mysql -u root -p
```
```sql
CREATE DATABASE IF NOT EXISTS MovieProduction;
USE MovieProduction;
CREATE TABLE IF NOT EXISTS ACTOR (
    Actor_ID INT PRIMARY KEY,
    ActorName VARCHAR(100),
    Gender VARCHAR(10),
    Nationality VARCHAR(50),
    Fee DECIMAL(10, 2)
);
```

### Launch the Application:
```bash
python3 actor_crud_app.py
```

---

## 👨‍💻 Project Details
- **Developer**: Anish Mohanty
- **GitHub Repository**: [AnishMohanty10/dbms](https://github.com/AnishMohanty10/dbms)
- **License**: MIT
