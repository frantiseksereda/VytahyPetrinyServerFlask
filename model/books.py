import datetime as dt

from dataclasses import dataclass
from marshmallow import Schema, fields
from marshmallow import post_load
from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

@dataclass
class Book(Base):
    __tablename__ = 'books2'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    pages_num = Column(Integer)
    review = Column(String)
    date_added = Column(Date)

    def __init__(self, title, author, pages_num, review):
        self.title = title
        self.author = author
        self.pages_num = pages_num
        self.review = review
        self.date_added = dt.datetime.now()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class BookSchema(Schema):
    title = fields.Str()
    author = fields.Str()
    pages_num = fields.Int()
    review = fields.Str()
    date_added = fields.Date()

    @post_load
    def make_book(self, data, **kwargs):
        return Book(**data)
