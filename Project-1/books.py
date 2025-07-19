from fastapi import Body ,FastAPI

app = FastAPI()

BOOKS = [
    {'title' : 'Mouk adv' , 'author':'Cher','category':'slice of life'},
    {'title': 'aloo adv', 'author': 'Cher', 'category': 'slice of life'},
    {'title': 'fries adv', 'author': 'Cher2', 'category': 'slice of life2'},
    {'title': 'momos adv', 'author': 'Cher3', 'category': 'slice of life3'},

]
@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/book/query/")
async def author_book_query(author):
    author_books = []
    for book in BOOKS:
        if(book.get("author").casefold() == author):
            author_books.append(book)

    return author_books

@app.get("/book/path/{author}")
async def author_book(author):
    author_books = []
    for book in BOOKS:
        if(book.get("author").casefold() == author):
            author_books.append(book)

    return author_books

@app.get("/books/{book_title}")
async def read_books(book_title):
    for book in BOOKS:
        if(book.get("title").casefold() == book_title.casefold()):
            return book

@app.get("/books/")
async def get_category_by_query(category , title):
    books_to_return = []
    for book in BOOKS:
        if((book.get("category").casefold() == category.casefold()) and (book.get("title").casefold() == title.casefold())):
            books_to_return.append(book)

    return books_to_return

@app.post("/books/create-book")
async def create_book(new_book = Body()):
    BOOKS.append(new_book)
    return {"success" : f"new book{new_book} has been added successfully" ,
            "BOOKS" : BOOKS
            }

@app.put("/books/update-book")
async def update_book(update_book = Body()):
    for i in range(len(BOOKS)):
        if(update_book.get("title").casefold() == BOOKS[i].get("title").casefold()):
            BOOKS[i]=update_book

    return {
        "success" : "modified successfully",
        "BOOKS" : BOOKS
    }

@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title):
    for i in range(len(BOOKS)):
        if(book_title.casefold() == BOOKS[i].get("title").casefold()):
            BOOKS.pop(i)
            break

    return {
        "sucess" : f"Book with title {book_title} deleted successully",
        "BOOKS" : BOOKS
    }



