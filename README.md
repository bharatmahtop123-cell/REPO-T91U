# TaskFlow  Project

## What is TaskFlow?

TaskFlow is a lightweight task manager that lets users create, organise, complete, and delete tasks. It was built progressively — each week adding a new layer of functionality  from a static HTML page all the way to a tested, documented Flask REST API backed by SQLite.

---

## Project Structure

```
taskflow/
week1/
  hello world         First program html and css
 README.md           ←Environment setup guide
 
 week2/
tasks.py             Core task logic (OOP, CRUD)

 week3/

db_and_api.py       SQLite persistence + external API

week4/
 app.py               Flask REST API with validation & security
 
 week5/

 test_tasks.py        Unit tests (unittest / pytest)
 README.md            This file
```

---

## Weekly Breakdown

### Week 1  Foundation & Setup
- Installed Python, VS Code, Git, Flask
- normal hello world program
- Documented environment setup steps

### Week 2 Core Concepts
- Designed Task and TaskManager classes in Python
- Implemented full CRUD: create, read, update, delete
- Used clean OOP patterns and type hints throughout

### Week 3 Data & APIs
- Migrated task storage from in-memory to **SQLite**
- Integrated the **ZenQuotes public API** to fetch motivational quotes
- Added error handling for network failures (graceful fallback)

### Week 4  Optimisation & Security
- Built a **Flask REST API** with proper HTTP methods and status codes
- Added **input validation** (length limits, regex sanitisation)
- Added **security headers** (CSP, X-Frame-Options, X-Content-Type-Options)
- Refactored code for readability and separation of concerns

### Week 5  Testing & Deployment
- Wrote **10 unit tests** covering task creation, completion, filtering, deletion
- All tests pass with `python -m pytest week5/test_tasks.py -v`
- Added deployment notes for running on a VPS or PaaS like Railway/Render

### Week 6  
- Consolidated all work, polished code, wrote full documentation
- Prepared for GitHub and LinkedIn showcase

---

## How to Run

### 1. Clone the repo

git clone https://github.com/bharatmahtop123-cell/REPO-T91U.git


### 2. Set up virtual environment

python -m 

pip install flask requests pytest


### 3. Run the Flask API

cd week4
python app.py
# API running at http://localhost:5000


### 4. Run the tests

python -m pytest week5/test_tasks.py -v


---

## API Endpoints

| Method |         Endpoint       | Description 
|--------|      ----------        |-------------              
| GET    | `/tasks`               | List all tasks 
| GET    | `/tasks?done=0`        | List pending tasks only 
| POST   | `/tasks`               | Create a new task 
| PATCH  | `/tasks/<id>/complete` | Mark task as complete 
| DELETE | `/tasks/<id>`          | Delete a task 



---

## Tech Stack

| Layer           | Technology 
|-------          |-----------
| Frontend        | HTML5, CSS3 
| Backend         | Python 3.11, Flask
| Database        | SQLite 
| Testing         | unittest, pytest 
| External API    | ZenQuotes API 
| Version Control | Git / GitHub 

---

## What I Learned

- How to structure a Python project cleanly using OOP
- How to persist data with SQLite and use parameterised queries to prevent SQL injection
- How to build and consume REST APIs
- The importance of input validation and security headers in web apps
- How to write meaningful unit tests that catch real bugs

---

#Built by [Bharat Mahto]  Intern Career Path, 
