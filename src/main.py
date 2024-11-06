from fastapi import FastAPI, Depends, HTTPException
from bson.objectid import ObjectId

from .db import db
from .models import PyObjectId, Book, UpdateBookModel


app = FastAPI()

books_collection = db.get_collection("books")

@app.get("/books")
async def list_books():
    query_res = await books_collection.find().to_list()
    return list(map(lambda item: Book(**item), query_res))

@app.post("/books")
async def add_book(book: Book):
    new_book = await books_collection.insert_one(book.model_dump(by_alias=True, exclude=["id"]))
    return f"Book with id: {new_book.inserted_id} had been created"


@app.get("/books/{id}")
async def retrieve_single_book(id: PyObjectId):
    book = await books_collection.find_one({"_id": ObjectId(id)})
    if (book is not None):
        return Book(**book)
    return HTTPException(status_code=404, detail=f"Book with id: {id} does not exist")

@app.put("/books/{id}")
async def update_book(id: PyObjectId, book: UpdateBookModel):
    # remove unused fields
    book_dict = {k: v for k, v in filter(lambda item: item[1] is not None, dict(book).items())}
    update_res = await books_collection.update_one({"_id": ObjectId(id)}, {"$set": book_dict})
    if (update_res.matched_count > 0):
        return "Book updated successfully"
    return HTTPException(status_code=404, detail=f"Book with id: {id} does not exist")

@app.delete("/books/{id}")
async def delete_book(id: PyObjectId):
    del_query = await books_collection.delete_one({"_id": ObjectId(id)})
    return id
