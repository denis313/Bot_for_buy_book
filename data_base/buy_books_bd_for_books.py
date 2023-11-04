import sqlite3

# with sqlite3.connect("data_base/book_shop.db") as con:
#     cur = con.cursor()
#     cur.execute('''CREATE TABLE books(
#         id_book INTEGER PRIMARY KEY AUTOINCREMENT,
#         name VARCHAR,
#         author VARCHAR,
#         description VARCHAR,
#         price VARCHAR,
#         photo VARCHAR
#     )''')


def get_all_books() -> list:
    try:
        with sqlite3.connect("data_base/book_shop.db") as con:
            cur = con.cursor()
            books = cur.execute("SELECT id_book, name, author, description, price, photo FROM books").fetchall()
            con.commit()
        return books
    except Exception as e:
        print(e)


def get_book(id_book: int) -> tuple:
    try:
        with sqlite3.connect("data_base/book_shop.db") as con:
            cur = con.cursor()
            book = cur.execute("SELECT name, author, price, photo FROM books "
                               "WHERE id_book = ?", (id_book,)).fetchone()
        return book
    except Exception as e:
        print(e)


def search_for_book_in_bd(name: str, author: str) -> tuple:
    try:
        with sqlite3.connect("data_base/book_shop.db") as con:
            cur = con.cursor()
            book = cur.execute("SELECT name, author, description, price, photo FROM books "
                               "WHERE name=? AND author=?",
                               (name.lower(), author.lower())).fetchone()
            con.commit()
        return book
    except Exception as e:
        print(e)


def add_new_book(name: str, author: str, description: str, price: int, photo: str):
    try:
        with sqlite3.connect("data_base/book_shop.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO main.books(name, author, description, price, photo) VALUES(?,?,?,?,?)",
                        (name.lower(), author.lower(), description.lower(), price, photo))
            con.commit()
    except Exception as e:
        print(e)


def delete_book(id_book: int):
    try:
        with sqlite3.connect("data_base/book_shop.db") as con:
            cur = con.cursor()
            cur.execute("DELETE FROM books WHERE id_book = ?", (id_book,))
    except Exception as e:
        print(e)


def change_book(id_book: int):
    pass
