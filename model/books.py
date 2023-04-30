import datetime as dt

from marshmallow import Schema, fields


class Book(object):
    def __init__(self, title, author, pages_num, review, date_added):
        self.title = title
        self.author = author
        self.pages_num = pages_num
        self.review = review
        self.date_added = date_added

    def __repr__(self):
        return '<Book(name={self.title!r})>'.format(self=self)


class BookSchema(Schema):
    title = fields.Str()
    author = fields.Str()
    pages_num = fields.Int()
    review = fields.Str()
    date_added = fields.Date()
