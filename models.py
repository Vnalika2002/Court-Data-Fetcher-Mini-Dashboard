import sqlite3

def init_db():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS queries
                 (id INTEGER PRIMARY KEY,
                  case_type TEXT,
                  case_number TEXT,
                  filing_year TEXT,
                  response_html TEXT)''')
    conn.commit()
    conn.close()

def log_query(case_type, case_number, filing_year, response_html):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("INSERT INTO queries (case_type, case_number, filing_year, response_html) VALUES (?, ?, ?, ?)",
              (case_type, case_number, filing_year, response_html))
    conn.commit()
    conn.close()
