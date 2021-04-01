from fastapi import FastAPI, Body, Header, File
from models.user import User
from models.author import Author
from models.book import Book
from starlette.status import HTTP_201_CREATED

app_v1 = FastAPI(openapi_prefix='/v1')

@app_v1.post("/user", status_code = HTTP_201_CREATED)
async def post_user(user : User, x_custom : str = Header(...)):
    return {"request_body" : user, "custom headers" : x_custom}

@app_v1.get("/user")
async def get_user_validation(password:str):
    return {"query parameter" : password}

@app_v1.get("/book/{isbn}", response_model = Book, response_model_include=["name","year"], response_model_exclude=["author"])
async def get_book_with_isbn(isbn : str):
    author_dict = {
        "name" : "author1",
        "book" : ["book1", "book2"]
    }
    author = Author(**author_dict)
    book_dict = {
        "isbn" : isbn,
        "name" : "book1",
        "author" : author,
        "year" : 2021 
    }
    book = Book(**book_dict)
    return book

@app_v1.get("/author/{id}/books")
async def get_authors_book(id : int, category : str, order : str = "asc"):
    return {"query changeable + paramater", f"{id} {category} {order}"}

@app_v1.patch("/author/name")
async def patch_author_name(name : str = Body(...,embed=True)):
    return {"name in body" : name}

@app_v1.post("/user/author")
async def post_user_and_author(user : User, author : Author):
    return {"user" : user, "author" : author}

@app_v1.post("/user/photo")
async def upload_user_photo(profile_photo : bytes = File(...)):
    return {"file size ":  len(profile_photo)}