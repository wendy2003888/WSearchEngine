# -*- coding: utf-8 -*- 

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import DB_URI



engine = create_engine(DB_URI, encoding='utf-8',echo=True, pool_recycle=10)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()

BaseModel = declarative_base()
