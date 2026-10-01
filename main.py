from fastapi import FastAPI, status,Depends
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from typing import List,Optional
from database import sessionLocal,engine
from models import Book,Base
from seed import init_db
from sqlalchemy.orm import Session
Base.metadata.create_all(bind=engine)

app = FastAPI()
@app.on_event("startup")
def startup_event():
    db=sessionLocal()
    try:
        init_db(db)
    finally:
        db.close()
def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()
class BookSchema(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
    class Config:
        form_attributes:True
class BookUpdateModel(BaseModel):
    title: Optional[str]=None
    author: Optional[str]=None
    publisher: Optional[str]=None
    published_date: Optional[str]=None
    page_count: Optional[int]=None
    language: Optional[str]=None

class BookCreateSchema(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


@app.get('/books')
async def get_all_books(db:Session=Depends(get_db))->List[BookSchema]:
    books=db.query(Book).all()
    return books

@app.post('/books',status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data:BookCreateSchema,db:Session=Depends(get_db))->BookSchema:
    new_book=Book(**book_data.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.patch('/books/{book_id}',status_code=status.HTTP_202_ACCEPTED)
async def update_book(book_id:int,book_update_data:BookUpdateModel,db:Session=Depends(get_db))->BookSchema:
    book=db.query(Book).filter(Book.id==book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="book not found")
    update_data=book_update_data.model_dump(exclude_unset=True)
    for field,value in update_data.items():
        setattr(book,field,value)
    db.commit()
    db.refresh(book)
    db.close()
    return book

@app.delete('/delete/{book_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:int,db:Session=Depends(get_db)):
    book=db.query(Book).filter(Book.id==book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="book not found")
    db.delete(book)
    db.commit()
    db.close()