import os

import requests

urlNameGet = "http://127.0.0.1:5000/expenses"
response = requests.get(url=urlNameGet)
print(response.text)

urlNameBalance = "http://127.0.0.1:5000/balance"
response = requests.get(url=urlNameBalance)
print(response.text)

urlBooks = "http://127.0.0.1:5000/books"
response = requests.get(url=urlBooks)
print(response.text)


#print(os.environ.get('DB_USERNAME'))