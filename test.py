from fastapi import FastAPI , HTTPException
from fastapi.responses import JSONResponse
import sqlite3
from pydantic import BaseModel

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
    cursor.execute("DELETE  FROM books WHERE id = ?" , (id ,))
    conn.commit()
    conn.close()
def UPDATE(name , author , status , id):
    conn = get_conn()
    curser = conn.cursor()
    curser.execute("""
UPDATE books SET name = ?,author = ?,status = ? WHERE id = ?
""" , (name , author , status , id))
    conn.commit()
    conn.close()
def book_exists_for_update(book_id: int) -> bool:
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM books WHERE id = ?", (book_id,))
    row = cursor.fetchone()
    conn.close()
    return row is not None
    
class Books(BaseModel):
    name : str
    author : str
    status : str

@app.get("/")
def online():
  return(JSONResponse("massage: books api is ready to use"))
@app.post("/books")
def add_book(book : Books):
    if not book.author or not book.name:
        raise HTTPException(
            status_code=400 ,
            detail= "massage : name and author must not be empty"
        )
    
    elif book.status not in ["present", "absent", "PRESENT", "ABSENT", "Present", "Absent"]:
        raise HTTPException(
            status_code=400 ,
            detail= "massage : status most be (present) or (absent)"
        )
    else:
        ADD(book.name , book.author , book.status)
        return JSONResponse(
           status_code=200 ,
           content={"message": "book was added"}
        )
@app.get("/books/{id}")
def get_book(id: int):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, author, status FROM books WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "id": row[0],
            "name": row[1],
            "author": row[2],
            "status": row[3]
        }
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Book with id {id} not found"
        )
@app.put("/books/{id}")
def update_book(book : Books , id=id):
    if not book.author or not book.name:
        raise HTTPException(
            status_code=400 ,
            detail= "massage : name and author must not be empty"
        )
    
    elif book.status not in ["present", "absent", "PRESENT", "ABSENT", "Present", "Absent"]:
        raise HTTPException(
            status_code=400 ,
            detail= "message : status most be (present) or (absent)"
        )
    elif not book_exists_for_update(id):
        raise HTTPException(
            status_code=404 ,
            detail=f"Book with id {id} not found"
        )
    else:
        UPDATE(book.name , book.author , book.status , id)
        return JSONResponse(
            status_code=200 ,
            content={"message" : "book has been updated"}
        )
@app.delete("/books/{id}")
def delete_book(id: int):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM books WHERE id = ?", (id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail=f"Book with id {id} not found"
        )
    else:
        REMOVE(id)
        return JSONResponse(
            status_code=200 ,
            content={"message" : "book has been deleted"}
            )
@app.get("/all_books")
def get_all_books():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, author, status FROM books")
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return {"message": "no books found"}
    else:
        return [
        {
            "id": row[0],
            "name": row[1],
            "author": row[2],
            "status": row[3]
        }
        for row in rows
    ]