import sqlite3


'''   
        Создание новых пользователей
'''


def new_user(user_id: int):
    user_id = user_id
    count_books = 0
    total_amount = 0
    try:
        with sqlite3.connect("data_base/book_shop.db") as con:
            cur = con.cursor()
            user = cur.execute("SELECT user_id FROM users WHERE user_id = ?",
                               (user_id,)).fetchone()
            if user is None:
                cur.execute("INSERT INTO users VALUES(?,?,?,?)",
                            (user_id, count_books, 'Книги: ', total_amount), )
    except Exception as e:
        print(e)


'''   
        Получение информации о пользователе
'''


def get_user_data(user_id: int) -> tuple:
    user_id = user_id
    try:
        with sqlite3.connect("data_base/book_shop.db") as con:
            cur = con.cursor()
            user_data = cur.execute("SELECT user_id, count_books, books_basket, total_amount FROM users "
                                    "WHERE user_id = ?",
                               (user_id,)).fetchone()
        return user_data
    except Exception as e:
        print(e)


'''   
        Создание новых пользователей
'''


def getting_information_from_the_cart(user_id: int) -> tuple:
    user_id = user_id
    try:
        with sqlite3.connect("data_base/book_shop.db") as con:
            cur = con.cursor()
            list_books = cur.execute("SELECT books_basket, total_amount FROM users WHERE user_id = ?",
                                    (user_id,)).fetchone()
        return list_books
    except Exception as e:
        print(e)


'''   
        Получение информации о корзине пользователя
'''


def update_basket(user_id: int, name: str, author: str, price: int):
    data = getting_information_from_the_cart(user_id)
    book_basket = f'{data[0]} {name} {author} {price};'
    total_amount = data[1] + int(price)
    try:
        with sqlite3.connect("data_base/book_shop.db") as con:
            cur = con.cursor()
            cur.execute("UPDATE users SET books_basket = ?, total_amount = ? WHERE user_id = ?",
                        (book_basket, total_amount, user_id,))
    except Exception as e:
        print(e)


def delete_basket(id_basket: int):
    try:
        with sqlite3.connect("data_base/book_shop.db") as con:
            cur = con.cursor()
            cur.execute("DELETE FROM users WHERE id_book = ?", (id_basket,))
    except Exception as e:
        print(e)
# print(update_basket(user_id=1087502760, name='Библия', author='Бог', price=1000000000))
