import datetime as dt

from marshmallow import Schema, fields
from marshmallow import post_load


class Book(object):
    def __init__(self, title, author, pages_num, review):
        self.title = title
        self.author = author
        self.pages_num = pages_num
        self.review = review
        self.date_added = dt.datetime.now()

    def __repr__(self):
        return '<Book(name={self.title!r})>'.format(self=self)


class BookSchema(Schema):
    title = fields.Str()
    author = fields.Str()
    pages_num = fields.Int()
    review = fields.Str()
    date_added = fields.Date()

    @post_load
    def make_book(self, data, **kwargs):
        return Book(**data)
