from fastapi import FastAPI
import sqlite3

app = FastAPI()

DB_PATH = "data.sqlite"

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# ساخت جدول student هنگام شروع اپ
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
