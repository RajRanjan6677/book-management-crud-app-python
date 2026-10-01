from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
DATABASE_URL="mysql+pymysql://root:raj*(18092005)M#D@localhost:3306/book"
engine=create_engine(DATABASE_URL)#echo=True?
sessionLocal=sessionmaker(bind=engine)
Base=declarative_base()