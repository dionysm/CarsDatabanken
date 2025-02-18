import sqlite3


def add_insert():
    connection = sqlite3.connect('autowelt.db')
    cursor = connection.cursor()
    cursor.executemany("INSERT INTO hersteller (name) VALUES (?)",
                       [('Volkswagen',), ('BMW',), ('Audi',), ('Mercedes',), ('Porsche',)])

    cursor.executemany("INSERT INTO autos (model, jahr, price, hersteller_id) VALUES (?, ?, ?, ?)",
                       [('Volkswagen Golf', 2019, 100000, 1),
                        ('BMW M3', 2019, 150000, 2),
                        ('Audi A4', 2019, 120000, 3),
                        ('Mercedes-Benz C-Class', 2019, 180000, 4),
                        ('Porsche 911', 2019, 160000, 5)])

    cursor.executemany("INSERT INTO anbieter (name) VALUES (?)",
                       [('Habert',), ('Bernard',), ('Albert',), ('Maria',), ('Pannyellow',)])

    cursor.executemany("INSERT INTO angebot (angebot_preis, beschreibung, auto_id, anbieter_id) VALUES (?, ?, ?, ?)",
                       [(100000, 'Habert: Volkswagen Golf, 2019, 100000', 1, 1),
                        (150000, 'Bernard: BMW M3, 2019, 150000', 2, 2),
                        (120000, 'Albert: Audi A4, 2019, 120000', 3, 3),
                        (180000, 'Maria: Mercedes-Benz C-Class, 2019, 180000', 4, 4),
                        (160000, 'Pannyellow: Porsche 911, 2019, 160000', 5, 5)])

    connection.commit()
    connection.close()
    print("Datensätze erstellt")

def create():
    connection = sqlite3.connect('autowelt.db')
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        username TEXT NOT NULL, 
        password TEXT NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hersteller (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name VARCHAR(50) NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS autos (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        model VARCHAR(50) NOT NULL,
        jahr INTEGER NOT NULL, 
        price INT, 
        hersteller_id INTEGER, 
        FOREIGN KEY (hersteller_id) REFERENCES hersteller(id) 
        ON DELETE CASCADE ON UPDATE CASCADE
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS anbieter (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name VARCHAR(50) NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS angebot (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        angebot_preis INT NOT NULL,
        beschreibung TEXT NOT NULL,
        auto_id INTEGER, 
        anbieter_id INTEGER, 
        FOREIGN KEY (auto_id) REFERENCES autos(id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (anbieter_id) REFERENCES anbieter(id) 
        ON DELETE CASCADE ON UPDATE CASCADE
    )""")
    print("Database erstellt")

    connection.commit()
    connection.close()

# -------------------------------
# -------------------------- RUN
# -------------------------------
create()
add_insert()
