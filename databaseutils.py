import sqlite3


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


def add_insert():
    connection = sqlite3.connect('autowelt.db')
    cursor = connection.cursor()

    # Liste der 51 Automarken (Hersteller)
    manufacturers = [
        'Volkswagen', 'BMW', 'Audi', 'Mercedes', 'Porsche',
        'Fiat', 'Toyota', 'Honda', 'Nissan', 'Ford',
        'Chevrolet', 'Subaru', 'Mazda', 'Hyundai', 'Kia',
        'Mitsubishi', 'Renault', 'Peugeot', 'Citroen', 'Volvo',
        'Land Rover', 'Jaguar', 'Lexus', 'Acura', 'Infiniti',
        'Dodge', 'Jeep', 'GMC', 'Cadillac', 'Tesla',
        'Opel', 'Skoda', 'SEAT', 'Suzuki', 'MINI',
        'Alfa Romeo', 'Aston Martin', 'Bentley', 'Bugatti', 'Ferrari',
        'Lamborghini', 'Maserati', 'McLaren', 'Rolls Royce', 'Saab',
        'Hummer', 'Geely', 'Chery', 'BYD', 'Mahindra', 'Tata Motors'
    ]

    # Für jede Automarke gibt es ein passendes Modell.
    # Die ersten 5 Einträge (alte Werte) bleiben erhalten,
    # ab Hersteller Nr. 6 wird jeweils ein Modell mit passenden Werten eingesetzt.
    auto_entries = [
        ('Golf 5', 2019, 100000, 1),
        ('M3', 2019, 150000, 2),
        ('A4', 2019, 120000, 3),
        ('C-Class', 2019, 180000, 4),
        ('911', 2019, 160000, 5),
        ('500', 2020, 15000, 6),  # Fiat
        ('Corolla', 2020, 20000, 7),  # Toyota
        ('Civic', 2020, 21000, 8),  # Honda
        ('Altima', 2020, 22000, 9),  # Nissan
        ('Mustang', 2020, 30000, 10),  # Ford
        ('Camaro', 2020, 35000, 11),  # Chevrolet
        ('Impreza', 2020, 25000, 12),  # Subaru
        ('MX-5', 2020, 27000, 13),  # Mazda
        ('Elantra', 2020, 19000, 14),  # Hyundai
        ('Optima', 2020, 21000, 15),  # Kia
        ('Lancer', 2020, 18000, 16),  # Mitsubishi
        ('Clio', 2020, 17000, 17),  # Renault
        ('208', 2020, 16000, 18),  # Peugeot
        ('C3', 2020, 15000, 19),  # Citroen
        ('XC90', 2020, 50000, 20),  # Volvo
        ('Range Rover', 2020, 70000, 21),  # Land Rover
        ('XF', 2020, 45000, 22),  # Jaguar
        ('IS', 2020, 40000, 23),  # Lexus
        ('TLX', 2020, 38000, 24),  # Acura
        ('Q50', 2020, 39000, 25),  # Infiniti
        ('Charger', 2020, 32000, 26),  # Dodge
        ('Wrangler', 2020, 33000, 27),  # Jeep
        ('Sierra', 2020, 34000, 28),  # GMC
        ('Escalade', 2020, 75000, 29),  # Cadillac
        ('Model S', 2020, 80000, 30),  # Tesla
        ('Corsa', 2020, 16000, 31),  # Opel
        ('Octavia', 2020, 22000, 32),  # Skoda
        ('Leon', 2020, 21000, 33),  # SEAT
        ('Swift', 2020, 14000, 34),  # Suzuki
        ('Cooper', 2020, 23000, 35),  # MINI
        ('Giulia', 2020, 37000, 36),  # Alfa Romeo
        ('DB11', 2020, 200000, 37),  # Aston Martin
        ('Continental GT', 2020, 250000, 38),  # Bentley
        ('Chiron', 2020, 3000000, 39),  # Bugatti
        ('488', 2020, 280000, 40),  # Ferrari
        ('Huracan', 2020, 300000, 41),  # Lamborghini
        ('Ghibli', 2020, 75000, 42),  # Maserati
        ('720S', 2020, 280000, 43),  # McLaren
        ('Phantom', 2020, 450000, 44),  # Rolls Royce
        ('9-3', 2020, 22000, 45),  # Saab
        ('H2', 2020, 40000, 46),  # Hummer
        ('Emgrand', 2020, 14000, 47),  # Geely
        ('Tiggo', 2020, 13000, 48),  # Chery
        ('Tang', 2020, 30000, 49),  # BYD
        ('XUV500', 2020, 25000, 50),  # Mahindra
        ('Nano', 2020, 5000, 51)
        # Tata Motors
    ]

    # Anbieter (Verkäufer) – hier nehmen wir 5 Beispielnamen
    vendor_names = ["Habert", "Bernard", "Albert", "Maria", "Pannyellow"]

    # User List
    user_names = ["Dejan", "Adem", "Dmytro", "Dio", "Magdalena", "Roman", "Alexander"]


    # Hersteller einfügen
    cursor.executemany("INSERT INTO hersteller (name) VALUES (?)", [(m,) for m in manufacturers])

    # Autos einfügen
    cursor.executemany("INSERT INTO autos (model, jahr, price, hersteller_id) VALUES (?, ?, ?, ?)", auto_entries)

    # Anbieter einfügen
    cursor.executemany("INSERT INTO anbieter (name) VALUES (?)", [(v,) for v in vendor_names])

    # Für user / anbieter
    #cursor.executemany("INSERT INTO user (name) VALUES (?)", [(v,) for v in vendor_names])

    # Für jedes Auto wird ein Angebot generiert.
    # Wir gehen davon aus, dass die Autonummer (auto_id) der Reihenfolge im auto_entries entspricht.
    angebot_entries = []
    for i, (model, jahr, price, hersteller_id) in enumerate(auto_entries, start=1):
        # Wähle den Anbieter zyklisch aus der vendor_names-Liste
        anbieter_id = (i - 1) % len(vendor_names) + 1
        vendor = vendor_names[anbieter_id - 1]
        # Hole den Hersteller-Namen (Hersteller-ID entspricht dem Index+1 in der manufacturers-Liste)
        manufacturer = manufacturers[hersteller_id - 1]
        description = f"{vendor}: {manufacturer} {model}, {jahr}, {price}"
        angebot_entries.append((price, description, i, anbieter_id))

    cursor.executemany(
        "INSERT INTO angebot (angebot_preis, beschreibung, auto_id, anbieter_id) VALUES (?, ?, ?, ?)",
        angebot_entries
    )

    connection.commit()
    connection.close()
    print("Datensätze erstellt")


# -------------------------------
# -------------------------- RUN
# -------------------------------
create()
add_insert()
