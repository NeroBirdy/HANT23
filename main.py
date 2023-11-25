import eel
import sqlite3
import werkzeug

eel.init("templates")

@eel.expose
def short_info(Block_number):
    connection = sqlite3.connect('db/events.db')
    cursor = connection.cursor()

    cursor.execute('SELECT city, date, type FROM info LIMIT ?, 1', (Block_number - 1,))
    info = list(cursor.fetchone())

    return tuple(info)
    connection.close()

@eel.expose
def short_desc(Block_number):
    connection = sqlite3.connect('db/events.db')
    cursor = connection.cursor()

    cursor.execute('SELECT sDesc FROM info LIMIT ?, 1', (Block_number - 1,))
    info = cursor.fetchone()

    return info

    connection.close()

@eel.expose
def Block_full(Block_number):
    connection = sqlite3.connect('db/events.db')
    cursor = connection.cursor()

    cursor.execute('SELECT address, fDesc, category, time, org, age FROM info LIMIT ?, 1', (Block_number - 1,))
    info = list(cursor.fetchone())

    return tuple(info)

    connection.close()

is_login = False

@eel.expose
def checkLogin():
    return is_login

def createUserDB():
    user_db = sqlite3.connect("db/users.db")
    user_db.execute("""
    CREATE TABLE USERS(
        id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        surname TEXT,
        login TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL
    );
    """)
    user_db.close()


@eel.expose
def register(f_name, l_name, surname, login, password):
    db = sqlite3.connect('db/users.db')
    cursor = db.cursor()
    password_hash = werkzeug.security.generate_password_hash(password)
    line_count = int(db.execute("SELECT COUNT(*) FROM USERS").fetchone()[0])
    cursor.execute("INSERT INTO USERS (id, first_name, last_name, surname, login, password_hash) VALUES(?, ?, ?, ?, ?, ?)", (line_count + 1, f_name, l_name, surname, login, password_hash))
    db.commit()
    cursor.close()
    db.close()

@eel.expose
def login(login, password):
    db = sqlite3.connect('db/users.db')
    password_hash = db.execute("select password_hash from users where login = (?)", (login,)).fetchone()[0]
    name = db.execute("select first_name from users where login = (?)", (login,)).fetchone()[0]
    db.close()
    if (werkzeug.security.check_password_hash(password_hash,password)):
        is_login = True
        return (name, True)


if __name__ == "__main__":
    eel.start("home.html",size=(428,926))