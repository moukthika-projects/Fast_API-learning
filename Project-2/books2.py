from fastapi import Body , FastAPI , Path , Query , HTTPException
from pydantic import BaseModel , Field
from typing import Optional
from starlette import status

app = FastAPI()

class Book:
    id : int
    title : str
    author : str
    description : str
    rating : int
    published_date: int

    def __init__(self , id , title, author , description , rating , published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1 , max_length=100)
    rating: int = Field(gt=0 , lt=6)
    published_date: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A new description of a book",
                "rating": 5,
                'published_date': 2029
            }
        }
    }


BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5 , 2002),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5 , 2001),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5 , 1968),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2 , 1974),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3 , 1989),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1 , 2001)
]

print(type(BOOKS[0].id))



@app.get("/books" , status_code= status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/date1/" , status_code=status.HTTP_200_OK)
async def get_published_date(date : int):
    filter_books = []
    for book in BOOKS:
        if book.published_date == date:
            filter_books.append(book)

    return filter_books


@app.get("/books/rating/{rating}" , status_code=status.HTTP_200_OK)
async def get_book_rating(rating: int = Path(gt = 0)):
    rating_books = []
    for book in BOOKS:
        if book.rating == rating:
            rating_books.append(book)
    return rating_books


@app.get("/books/{book_id}" , status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id:int):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404 , detail="404 item not found")

@app.post("/create-book" , status_code=status.HTTP_201_CREATED)
async def create_book(book_request : BookRequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))

@app.put("/update/update-book" , status_code=status.HTTP_204_NO_CONTENT)
async def update_book(data : BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == data.id:
            BOOKS[i] = data
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404 , detail="not found")

@app.delete("/delete/" , status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id : int = Path(gt = 0) ):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            return
    if not book_changed:
        raise HTTPException(status_code=404 , detail="not found")


def find_book_id(book : Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1

    return book


