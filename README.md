# Jdev26 RDBMS Demo

## Overview
This project is a **simple relational database management system (RDBMS)** built in Python, designed for educational and portfolio purposes. It demonstrates:

- A **REPL interface** for running SQL-like commands (`CREATE`, `INSERT`, `SELECT`, `UPDATE`, `DELETE`)
- A **dynamic web demo** using Flask, allowing CRUD operations in the browser
- Implementation of **Database** and **Table** classes with **primary key** and **unique key** support
- Basic **indexing** for fast lookups
- A **polished UI** with centered forms and dynamic table updates

This project was built as part of the **Pesapal JDEV26 Developer Challenge**.

---

## Project Structure
Jdev26-rdbms-demo/
├─ rdbms/
│ ├─ init.py
│ ├─ database.py # Database class managing multiple tables
│ ├─ table.py # Table class with CRUD operations and indexing
│ └─ repl.py # Interactive REPL for SQL-like commands
├─ app.py # Flask web app demo
├─ README.md
├─ requirements.txt # Python dependencies (Flask)
└─ venv/ # Optional virtual environment


---

## Features

### REPL Interface
- SQL-like commands:
  - `CREATE TABLE`
  - `INSERT`
  - `SELECT`
  - `UPDATE`
  - `DELETE`
- Supports **primary keys**, **unique keys**, and basic indexing
- Interactive mode (`exit` to quit)

### Dynamic Web Demo
- Add, update, and delete users from the browser
- Table updates instantly using JavaScript (AJAX)
- Clear success/error messages
- Clean, centered layout

### Extendable Design
- Supports multiple tables
- Can be extended to support joins, sorting, searching, and analytics

---

## Getting Started
### 1. Clone the Repository
```bash
git clone git@github.com:hesbonangwenyi606/Jdev26-rdbms-demo.git
cd Jdev26-rdbms-demo

## Setup Virtual Environment 
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## How to Use
REPL Interface
cd rdbms
python3 -m rdbms.repl

## Example Commands
CREATE TABLE users (id INT PRIMARY, name TEXT);
INSERT INTO users VALUES (1, 'Alice');
INSERT INTO users VALUES (2, 'Bob');
SELECT * FROM users;
UPDATE users SET name='Charlie' WHERE id=1;
DELETE FROM users WHERE id=2;
exit

## Web Demo
Run the Flask app:
python3 app.py
Open your browser:  http://127.0.0.1:5000


## Web Features
Add User: Enter ID and Name
Update User Name: Enter ID and new name
Delete User: Enter ID
Instant updates with feedback messages

Screenshots

