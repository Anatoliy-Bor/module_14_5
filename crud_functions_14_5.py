import sqlite3

connection = sqlite3.connect('data_bases/Products.db')
cursor = connection.cursor()

def initiate_db():
    # cursor.execute('DELETE FROM Products')
    # cursor.execute('DELETE FROM Users')

    cursor.execute('''
	CREATE TABLE IF NOT EXISTS Products(
	id INTEGER PRIMARY KEY,
	title TEXT NOT NULL,
	description TEXT,
	price INTEGER NOT NULL

	)
	''')
    for i in range(1, 5):
        cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                       (f"Продукт {i}", f"Описание {i}", i * 100))

    cursor.execute('''
    	CREATE TABLE IF NOT EXISTS Users(
    	id INTEGER PRIMARY KEY,
    	username TEXT NOT NULL,
    	email TEXT NOT NULL,
    	age INTEGER NOT NULL,
    	balance INTEGER NOT NULL
    	)
    	''')
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON Users (email)")
    for i in range(1, 5):
        cursor.execute("INSERT INTO Users(username, email, age, balance) VALUES (?, ?, ?, ?) ",
                       (f"newuser{i}", f"example{i}ex@mail.ru", f"{i + 10}", 1000))

    connection.commit()
    connection.close()

def get_all_products():
    cursor.execute("SELECT id, title, description, price FROM Products")
    db = cursor.fetchall()
    return list(db)
    connection.commit()
    connection.close()

def add_user(username, email, age, balance):
    cursor.execute("INSERT INTO Users(username, email, age, balance) VALUES (?, ?, ?, ?) ",
                   (f"{username}", f"{email}ex@mail.ru", f"{age}", balance))
    connection.commit()
    connection.close()

def is_included(username):
    cursor.execute("SELECT username FROM Users WHERE username = ?", (username,))
    check_user = cursor.fetchone()
    if check_user is None:
        return False
    else:
        return True
    connection.commit()
    connection.close()




