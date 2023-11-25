import sqlite3
import eel

eel.init("templates")

@eel.expose
def short_info(Block_number):
    connection = sqlite3.connect('test.db')
    cursor = connection.cursor()

    cursor.execute('SELECT city, date, type FROM info LIMIT ?, 1', (Block_number - 1,))
    info = list(cursor.fetchone())

    return tuple(info)

    # Закрываем соединение
    connection.close()

@eel.expose
def short_desc(Block_number):
    connection = sqlite3.connect('test.db')
    cursor = connection.cursor()

    cursor.execute('SELECT sDesc FROM info LIMIT ?, 1', (Block_number - 1,))
    info = cursor.fetchone()

    return info

    connection.close()

@eel.expose
def Block_full(Block_number):
    connection = sqlite3.connect('test.db')
    cursor = connection.cursor()

    cursor.execute('SELECT address, fDesc, category, time, org, age FROM info LIMIT ?, 1', (Block_number - 1,))
    info = list(cursor.fetchone())

    return tuple(info)

    connection.close()

if __name__ == "__main__":
    eel.start("home.html",size=(420,820))
    