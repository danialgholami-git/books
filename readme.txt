for use this project:
write this command : uvicorn test:app --reload


APIs you can use:
GET/http://127.0.0.1:8000/all_books
*for see all books

POST/http://127.0.0.1:8000/books --write json:
{
    "name" : "books name " ,
    "author" : "books author" ,
    "status" : "present or absent"
}
*for add book

GET/http://127.0.0.1:8000/books/id
*for find book

PUT/http://127.0.0.1:8000/books/id --write json:
{
    "name" : "books name" ,
    "author" : "books author" ,
    "status" : "present or absent"
}
*for update books data

DELETE/http://127.0.0.1:8000/books?id=books id
*for delete book

TIP:when you run the project,the database with name=data.sqlite will be create