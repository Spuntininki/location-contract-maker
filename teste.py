from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {'title':'title One', 'description': 'Description One', 'Category': 'Science'},
    {'title':'title Two', 'description': 'Description Two', 'Category': 'History'},
    {'title':'title Three', 'description': 'Description Three', 'Category': 'Science'},
    {'title':'title Four', 'description': 'Description Four', 'Category': 'Romance'},
    {'title':'title Four', 'description': 'Description Four', 'Category': 'Romance'},
    {'title':'title Four', 'description': 'Description Four', 'Category': 'Science'},
    {'title':'title Five', 'description': 'Description Five', 'Category': 'thriller'},
    ]


@app.get('/get-books')
async def get_all_books():
    return BOOKS



@app.get('/get-books/mybook')
async def get_const_book():
    return BOOKS[4]

@app.get('/get-books/{title_name}')
async def get_title_book(title_name:str, category = ''):
    return_list = []
    for book in BOOKS:
        if category:
            if book['title'] == title_name and book['Category'] == category:
                return_list.append(book)
        else:
            if book['title'] == title_name:
                return_list.append(book)
    return return_list

@app.get('/get-books/{index}')
async def get_var_book(index: int):
    return BOOKS[index]

@app.post('/get-books/create-books')
async def create_new_book(book=Body()):
    BOOKS.append(book)
    return {'message': 'new book was created!'}


@app.put('/get-books/update-book')
async def update_book(updated_book=Body()):
    found = False
    for index, book in enumerate(BOOKS):
        if book.get('title') == updated_book.get('title'):
            found = True
            BOOKS[index] = updated_book
            return {'response':'Success',
                    'element updated': BOOKS[index]}
        