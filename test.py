from fastapi import FastAPI , status
import sqlite3

app = FastAPI()

DB_PATH = "data.sqlite"

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

conn = get_conn()
conn.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    author TEXT,
    status TEXT
);
""")
conn.commit()
conn.close()

def ADD(name , author , status):
   conn = get_conn()
   cursor = conn.cursor()
   cursor.execute("""
INSERT INTO books(name , author , status) VALUES
(?, ?, ?)
""", (name , author , status))
   conn.commit()
   conn.close()
def REMOVE(id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE  FROM books WHERE id = ?" , (id))
    conn.commit()
    conn.close