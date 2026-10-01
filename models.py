from database import Base
from sqlalchemy import Column,Integer,String
class Book(Base):
    __tablename__="books"
    id= Column(Integer,primary_key=True,unique=True,index=True)
    title= Column(String(50))
    author= Column(String(50))
    publisher= Column(String(50))
    published_date= Column(String(50))
    page_count= Column(Integer)
    language= Column(String(50))