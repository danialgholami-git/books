from typing import Union
from fastapi import FastAPI
import sqlite3

app = FastAPI()
conn = sqlite3.connect("data.sqlite")

conn.execute("""CREATE TABLE IF NOT EXISTS books(
   id INT PRIMARY KEY,
   name TEXT,
   author TEXT,
   status TEXT);
""")
conn.commit()
@app.get("/")