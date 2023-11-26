import eel
import sqlite3
import werkzeug

eel.init("templates")

db = sqlite3.connect("db/events.db")
cursor = db.cursor()


@eel.expose()
def search(text):
    test = cursor.execute(f"""SELECT * FROM info WHERE city LIKE ?
    OR address LIKE ? OR category LIKE ?
    OR date LIKE ? OR time LIKE ? OR org LIKE ? OR age LIKE ? OR type LIKE ?""", (f"%{text}%",f"%{text}%",f"%{text}%",f"%{text}%",
    f"%{text}%",f"%{text}%",f"%{text}%",f"%{text}%",))
    print(test.fetchall())

@eel.expose()
def getMap():
    test = cursor.execute("SELECT sDesc,category,lat,lon FROM info")
    return test.fetchall()

@eel.expose()
def filter(city,category,date,age,tp):
    if len(city)+len(category)+len(date)+len(age)+len(tp) == 0:
        temp = cursor.execute("SELECT * FROM info")
        arr = temp.fetchall()
        
        print(arr)
        return [arr,10000]
    line = f"SELECT * FROM info WHERE "
    count = 0
    fl = False
    for i in range(len(city)):
        if city[i] != "" :
            if count == 0 and fl == False:
                count+=1
                line += f"(city = '{city[i]}'"
                fl = True
            elif count == 0 and fl == True:
                count+=1
                line += f"city = '{city[i]}'"
            else:
                line += " OR "
                line += f"city = '{city[i]}'"
    if len(category) != 0 and fl == True:

        line += ") AND ("
        count = 0
    for i in range(len(category)):
        if category[i] != "":
            if count == 0 and fl == False:
                count+=1
                line += f"(category = '{category[i]}'"
                fl = True
            elif count == 0 and fl == True:
                count+=1
                line += f"category = '{category[i]}'"
            else:
                line += " OR "
                line += f"category = '{category[i]}'"
    if len(date) != 0 and fl == True:
        line += ") AND ("
        count = 0
    for i in range(len(date)):
        if date[i] != "":
            if count == 0 and fl == False:
                count+=1
                line += f"(date = '{date[i]}'"
                fl = True
            elif count == 0 and fl == True:
                count+=1
                line += f"date = '{date[i]}'"
            else:
                line += " OR "
                line += f"date = '{date[i]}'"
    if len(age) != 0 and fl == True:
        line += ") AND ("
        count = 0
    for i in range(len(age)):
        if age[i] != "":
            if count == 0 and fl == False:
                count+=1
                line += f"(age = '{age[i]}'"
                fl = True
            elif count == 0 and fl == True:
                count+=1
                line += f"age = '{age[i]}'"
            else:
                line += " OR "
                line += f"age = '{age[i]}'"
    if len(tp) != 0 and fl == True:
        line += ") AND ("
        count = 0
    for i in range(len(tp)):
        if tp[i] != "":
            if count == 0 and fl == False:
                count+=1
                line += f"(type = '{tp[i]}'"
                fl = True
            elif count == 0 and fl == True:
                count+=1
                line += f"type = '{tp[i]}'"
            else:
                line += " OR "
                line += f"tp = '{tp[i]}'"
    line += ")"
    print(line)
    test = cursor.execute(line)
    arr = test.fetchall()
    return [arr,len(arr)]

@eel.expose()
def select(attr):
    atr = []
    test = cursor.execute(f"SELECT {attr} FROM info")
    atr = list(set(test.fetchall()))
    for i in range(len(atr)):
        atr[i] = atr[i][0]
    return atr

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
    data = db.execute("select first_name, last_name, surname, login from users where login = (?)", (login,)).fetchall()
    db.close()
    data.append(True)
    if (werkzeug.security.check_password_hash(password_hash,password)):
        is_login = True
        return data


if __name__ == "__main__":
    eel.start("home.html",size=(428,926))