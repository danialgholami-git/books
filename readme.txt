for use this project:
write this command : uvicorn test:app --reload


APIs you can use:
POST/http://127.0.0.1:8000/books --write json:
{
    "name" : "books name "
    "author" : "books author"
    "status" : "present or absent"
}
*for add book

GET/http://127.0.0.1:8000/books?id=books id
*for find book

PUT/http://127.0.0.1:8000/books --write json:
{
    "id" : books id
    "name" : "books name"
    "author" : "books author"
    "status" : "present or absent"
}
*for update books data

DELETE/http://127.0.0.1:8000/books?id=books id
*for delete book