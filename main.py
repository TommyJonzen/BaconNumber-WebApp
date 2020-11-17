import sqlite3

db = sqlite3.connect('movies.db')

person = input("Enter a movie star: ")

db.execute("SELECT ")