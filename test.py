from fastapi import FastAPI , Form 
from fastapi.responses import HTMLResponse
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
    
@app.get("/" , response_class=HTMLResponse)
def html():
    site = """
    <!DOCTYPE html>
<html lang="fa">
<head>
  <meta charset="UTF-8">
  <title>خدمات</title>
  <style>
    body {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
      font-family: Arial, sans-serif;
      background-color: #f2f2f2;
    }

    h1 {
      margin-bottom: 30px;
    }

    .buttons {
      display: flex;
      gap: 15px;
    }

    button {
      padding: 10px 20px;
      font-size: 16px;
      cursor: pointer;
      border: none;
      background-color: #007BFF;
      color: white;
      border-radius: 5px;
      transition: background-color 0.3s ease;
    }

    button:hover {
      background-color: #0056b3;
    }
  </style>
</head>
<body>

  <h1>خدمات خود را انتخاب کنید</h1>

  <div class="buttons">
    <a href="/Add"><button>Add</button></a>
    <a href="/Remove"><button>Remove</button></a>
    <a href="/Update"><button>Update</button></a>
    <a href="/Detail"><button>Detail</button></a>
  </div>

</body>
</html>
"""
    return HTMLResponse(content=site)
@app.get("/Add" , response_class=HTMLResponse)
def add():
    site = """
    <!DOCTYPE html>
<html lang="fa">
<head>
  <meta charset="UTF-8">
  <title>فرم اطلاعات</title>
  <style>
    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      font-family: Arial, sans-serif;
      background-color: #f0f0f0;
    }

    .form-container {
      background-color: white;
      padding: 30px 40px;
      border-radius: 10px;
      box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
      text-align: center;
    }

    h1 {
      margin-bottom: 25px;
    }

    input[type="text"] {
      width: 100%;
      padding: 10px;
      margin: 10px 0;
      font-size: 16px;
      border: 1px solid #ccc;
      border-radius: 5px;
    }

    button {
      margin-top: 20px;
      padding: 10px 30px;
      font-size: 16px;
      border: none;
      background-color: #28a745;
      color: white;
      border-radius: 5px;
      cursor: pointer;
    }

    button:hover {
      background-color: #218838;
    }
  </style>
</head>
<body>

  <div class="form-container">
    <h1>اطلاعات زیر را وارد کنید</h1>
    <form method="POST" action="/Add/Enter">
      <input type="text" name="name" placeholder="name" required>
      <input type="text" name="author" placeholder="author" required>
      <input type="text" name="status" placeholder="status" required>
      <br>
      <button type="submit">Enter</button>
    </form>
  </div>

</body>
</html>
"""
    return(HTMLResponse(content=site))
@app.post("/Add/Enter" , response_class=HTMLResponse)
def add_sqlite(name:str = Form(...) , author:str = Form(...) , status:str = Form(...)):
    if status == "present" or status == "absent" or status == "ABSENT" or status == "PRESENT" or status == "Present" or status == "Absent":
      ADD(name , author , status)
      return """<html>
    <body style="text-align: center; padding-top: 50px; font-family: sans-serif;">
        <h2>اطلاعات با موفقیت ذخیره شد!</h2>
        <a href="/">بازگشت</a>
    </body>
    </html>
"""
    else:
      return """
    <html>
    <body style="text-align: center; padding-top: 50px; font-family: sans-serif;">
        <h2>اخطار!</h2>
        <p>status (most)= present or absent</p>
        <a href="/Add">بازگشت</a>
    </body>
    </html>
"""
     
@app.get("/Remove" , response_class=HTMLResponse())
def remove():
  site = """
      <!DOCTYPE html>
<html lang="fa">
<head>
  <meta charset="UTF-8">
  <title>فرم اطلاعات</title>
  <style>
    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      font-family: Arial, sans-serif;
      background-color: #f0f0f0;
    }

    .form-container {
      background-color: white;
      padding: 30px 40px;
      border-radius: 10px;
      box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
      text-align: center;
    }

    h1 {
      margin-bottom: 25px;
    }

    input[type="text"] {
      width: 100%;
      padding: 10px;
      margin: 10px 0;
      font-size: 16px;
      border: 1px solid #ccc;
      border-radius: 5px;
    }

    button {
      margin-top: 20px;
      padding: 10px 30px;
      font-size: 16px;
      border: none;
      background-color: #28a745;
      color: white;
      border-radius: 5px;
      cursor: pointer;
    }

    button:hover {
      background-color: #218838;
    }
  </style>
</head>
<body>

  <div class="form-container">
    <h1>اطلاعات زیر را وارد کنید</h1>
    <form method="POST" action="/Remove/Enter">
      <input type="number" name="id" placeholder="id" required>
      <br>
      <button type="submit">Enter</button>
    </form>
  </div>

</body>
</html>
"""
  return HTMLResponse(content=site)
@app.post("/Remove/Enter" , response_class=HTMLResponse)
def remove_sqlite(id:int = Form(...)):
  REMOVE(id)
  return """
  <html>
    <body style="text-align: center; padding-top: 50px; font-family: sans-serif;">
        <h2>اطلاعات با موفقیت ذخیره شد!</h2>
        <a href="/">بازگشت</a>
    </body>
    </html>
"""
@app.get("/Update" , response_class=HTMLResponse)
def update():
  site = """
      <!DOCTYPE html>
<html lang="fa">
<head>
  <meta charset="UTF-8">
  <title>فرم اطلاعات</title>
  <style>
    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      font-family: Arial, sans-serif;
      background-color: #f0f0f0;
    }

    .form-container {
      background-color: white;
      padding: 30px 40px;
      border-radius: 10px;
      box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
      text-align: center;
    }

    h1 {
      margin-bottom: 25px;
    }

    input[type="text"] {
      width: 100%;
      padding: 10px;
      margin: 10px 0;
      font-size: 16px;
      border: 1px solid #ccc;
      border-radius: 5px;
    }

    button {
      margin-top: 20px;
      padding: 10px 30px;
      font-size: 16px;
      border: none;
      background-color: #28a745;
      color: white;
      border-radius: 5px;
      cursor: pointer;
    }

    button:hover {
      background-color: #218838;
    }
  </style>
</head>
<body>

  <div class="form-container">
    <h1>اطلاعات زیر را وارد کنید</h1>
    <form method="POST" action="/Update/Enter">
      <input type="number" name="id" placeholder="id" required>
      <input type="text" name="name" placeholder="name" required>
      <input type="text" name="author" placeholder="author" required>
      <input type="text" name="status" placeholder="status" required>
      <br>
      <button type="submit">Enter</button>
    </form>
  </div>

</body>
</html>
"""
  return HTMLResponse(content=site)
@app.post("/Update/Enter" , response_class=HTMLResponse)
def update_sqlite(id:int = Form(...) , name:str = Form(...) , author:str = Form(...) , status:str = Form(...)):
  if status == "present" or status == "absent" or status == "ABSENT" or status == "PRESENT" or status == "Present" or status == "Absent":
    UPDATE(name , author , status , id)
    return """<html>
    <body style="text-align: center; padding-top: 50px; font-family: sans-serif;">
        <h2>اطلاعات با موفقیت ذخیره شد!</h2>
        <a href="/">بازگشت</a>
    </body>
    </html>
"""
  else:
    return """
    <html>
    <body style="text-align: center; padding-top: 50px; font-family: sans-serif;">
        <h2>اخطار!</h2>
        <p>status (most)= present or absent</p>
        <a href="/Add">بازگشت</a>
    </body>
    </html>
"""
@app.get("/Detail", response_class=HTMLResponse)
def detail_all():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    conn.close()
    table_html = """
    <html>
    <body style="text-align: center; padding-top: 50px; font-family: sans-serif;">
        <h2>لیست کتاب‌ها</h2>
        <table border="1" style="margin: auto; border-collapse: collapse; text-align: center;">
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Author</th>
                <th>Status</th>
            </tr>
    """
    for row in rows:
        table_html += f"""
            <tr>
                <td>{row[0]}</td>
                <td>{row[1]}</td>
                <td>{row[2]}</td>
                <td>{row[3]}</td>
            </tr>
        """
    table_html += """
        </table>
        <br>
        <a href="/">بازگشت</a>
    </body>
    </html>
    """

    return table_html