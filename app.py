from flask import Flask, jsonify, request
import psycopg2
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from model.expense import Expense, ExpenseSchema
from model.income import Income, IncomeSchema
from model.books import Book, BookSchema, Base
from model.transaction_type import TransactionType

app = Flask(__name__)

# engine = create_engine('postgresql://frantisek.sereda:S0cEAxmKkd6N@ep-gentle-frost-066984.eu-central-1.aws.neon.tech/pokusy')
conn_str = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']
conn_str_params = {pair.split('=')[0]: pair.split('=')[1] for pair in conn_str.split(' ')}
conn_str_to_use = 'postgresql://' + conn_str_params['user'] + ':' + conn_str_params['password'] + '@' + conn_str_params['host'] + '/' + conn_str_params['dbname']
engine = create_engine(conn_str_to_use)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
session = Session()



def get_db_connection():
    conn_str = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']
    conn_str_params = {pair.split('=')[0]: pair.split('=')[1] for pair in conn_str.split(' ')}
    conn = psycopg2.connect(
         host=conn_str_params['host'],
         database=conn_str_params['dbname'],
         user=conn_str_params['user'],
         password=conn_str_params['password']
     )

    # conn = psycopg2.connect(
    #         host="ep-gentle-frost-066984.eu-central-1.aws.neon.tech",
    #         database="pokusy",
    #         user="frantisek.sereda",
    #         password="S0cEAxmKkd6N")

    return conn


transactions = [
    Income('Salary', 5000),
    Income('Dividends', 200),
    Expense('pizza', 50),
    Expense('Rock Concert', 100)
]


@app.route('/incomes')
def get_incomes():
    schema = IncomeSchema(many=True)
    incomes = schema.dump(
        filter(lambda t: t.type == TransactionType.INCOME, transactions)
    )
    return jsonify(incomes)


@app.route('/incomes', methods=['POST'])
def add_income():
    income = IncomeSchema().load(request.get_json())
    transactions.append(income)
    return "", 201


@app.route('/expenses')
def get_expenses():
    schema = ExpenseSchema(many=True)
    expenses = schema.dump(
        filter(lambda t: t.type == TransactionType.EXPENSE, transactions)
    )
    return jsonify(expenses)


@app.route('/expenses', methods=['POST'])
def add_expense():
    expense = ExpenseSchema().load(request.get_json())
    transactions.append(expense)
    return "", 201


@app.route("/balance")
def get_balance():
    balance_to_return = 0
    for i in transactions:
        balance_to_return = balance_to_return + i.amount
    return jsonify(balance_to_return)


@app.route("/books")
def get_books():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM books;')
    books = cur.fetchall()
    schema = BookSchema(many=True)
    books_to_return = schema.dumps(books)

    print(books)
    print(books_to_return)

    return jsonify(books_to_return)

@app.route("/books2")
def get_books2():
    books = session.query(Book).all()
    schema = BookSchema(many=True)
    books_to_return = schema.dump(books)
    return jsonify(books_to_return)


@app.route("/add-book2", methods=["POST"])
def add_book2():
    title = str(request.json["title"])
    author = str(request.json["author"])
    pages_num = int(request.json["pages_num"])
    review = str(request.json["review"])

    book_to_add = Book(title=title, author=author, pages_num=pages_num, review=review)
    session.add(book_to_add)
    session.commit()
    session.close()

    return "", 201

@app.route("/add-book", methods=["POST"])
def add_book():
    title = str(request.json["title"])
    author = str(request.json["author"])
    pages_num = int(request.json["pages_num"])
    review = str(request.json["review"])

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO books (title, author, pages_num, review)'
                'VALUES (%s, %s, %s, %s)',
                (title, author, pages_num, review))
    conn.commit()
    cur.close()
    conn.close()

    return "", 201


if __name__ == '__main__':
    app.run(debug=True)
