import sqlite3
import random


def create():
    connection = sqlite3.connect('data/autowelt.db')
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
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username varchar(50) NOT NULL,
    password varchar(50) NOT NULL
    )""")
    print("Database erstellt")

    connection.commit()
    connection.close()


def add_insert():
    connection = sqlite3.connect('data/autowelt.db')
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

    # Hersteller einfügen
    cursor.executemany("INSERT INTO hersteller (name) VALUES (?)", [(m,) for m in manufacturers])

    # Echte Modelle pro Hersteller (mindestens 5 pro Marke)
    models_dict = {
        'Volkswagen': ['Golf', 'Passat', 'Polo', 'Tiguan', 'Touran'],
        'BMW': ['3er', '5er', '7er', 'X3', 'X5'],
        'Audi': ['A3', 'A4', 'A6', 'Q5', 'Q7'],
        'Mercedes': ['C-Klasse', 'E-Klasse', 'S-Klasse', 'GLC', 'GLE'],
        'Porsche': ['911', 'Cayenne', 'Macan', 'Panamera', 'Boxster'],
        'Fiat': ['500', 'Panda', 'Tipo', 'Doblo', '500X'],
        'Toyota': ['Corolla', 'Camry', 'Prius', 'RAV4', 'Hilux'],
        'Honda': ['Civic', 'Accord', 'CR-V', 'HR-V', 'Jazz'],
        'Nissan': ['Altima', 'Sentra', 'Maxima', 'Leaf', 'Qashqai'],
        'Ford': ['Focus', 'Fiesta', 'Mustang', 'Explorer', 'F-150'],
        'Chevrolet': ['Camaro', 'Corvette', 'Malibu', 'Silverado', 'Tahoe'],
        'Subaru': ['Impreza', 'Forester', 'Outback', 'WRX', 'Crosstrek'],
        'Mazda': ['Mazda3', 'Mazda6', 'CX-5', 'CX-9', 'MX-5'],
        'Hyundai': ['Elantra', 'Sonata', 'Tucson', 'Santa Fe', 'Kona'],
        'Kia': ['Rio', 'Optima', 'Sorento', 'Sportage', 'Stinger'],
        'Mitsubishi': ['Outlander', 'Outlander Sport', 'ASX', 'Eclipse Cross', 'Pajero Sport'],
        'Renault': ['Clio', 'Megane', 'Captur', 'Kadjar', 'Talisman'],
        'Peugeot': ['208', '308', '508', '2008', '3008'],
        'Citroen': ['C3', 'C4', 'C5 Aircross', 'C1', 'Berlingo'],
        'Volvo': ['S60', 'S90', 'XC60', 'XC90', 'V60'],
        'Land Rover': ['Range Rover', 'Discovery', 'Defender', 'Evoque', 'Freelander'],
        'Jaguar': ['XE', 'XF', 'XJ', 'F-Pace', 'E-Pace'],
        'Lexus': ['IS', 'ES', 'GS', 'RX', 'NX'],
        'Acura': ['TLX', 'MDX', 'RDX', 'ILX', 'RLX'],
        'Infiniti': ['Q50', 'Q60', 'QX50', 'QX60', 'QX80'],
        'Dodge': ['Charger', 'Challenger', 'Durango', 'Grand Caravan', 'Journey'],
        'Jeep': ['Wrangler', 'Grand Cherokee', 'Cherokee', 'Compass', 'Renegade'],
        'GMC': ['Sierra', 'Yukon', 'Canyon', 'Acadia', 'Terrain'],
        'Cadillac': ['CTS', 'Escalade', 'XT5', 'ATS', 'SRX'],
        'Tesla': ['Model S', 'Model 3', 'Model X', 'Model Y', 'Roadster'],
        'Opel': ['Corsa', 'Astra', 'Insignia', 'Mokka', 'Crossland'],
        'Skoda': ['Octavia', 'Fabia', 'Superb', 'Kodiaq', 'Scala'],
        'SEAT': ['Leon', 'Ibiza', 'Ateca', 'Tarraco', 'Alhambra'],
        'Suzuki': ['Swift', 'Vitara', 'Baleno', 'Celerio', 'Jimny'],
        'MINI': ['Cooper', 'Clubman', 'Countryman', 'Paceman', 'John Cooper Works'],
        'Alfa Romeo': ['Giulia', 'Stelvio', '4C', 'Giulietta', 'Spider'],
        'Aston Martin': ['DB11', 'Vantage', 'Rapide', 'Vanquish', 'DBS'],
        'Bentley': ['Continental GT', 'Flying Spur', 'Bentayga', 'Mulsanne', 'Azure'],
        'Bugatti': ['Chiron', 'Veyron', 'Divo', 'Centodieci', 'La Voiture Noire'],
        'Ferrari': ['488', 'Portofino', 'F8 Tributo', 'California', 'Roma'],
        'Lamborghini': ['Aventador', 'Huracan', 'Urus', 'Gallardo', 'Murcielago'],
        'Maserati': ['Ghibli', 'Levante', 'Quattroporte', 'GranTurismo', 'MC20'],
        'McLaren': ['720S', '570S', '650S', 'P1', 'Senna'],
        'Rolls Royce': ['Phantom', 'Ghost', 'Wraith', 'Dawn', 'Cullinan'],
        'Saab': ['9-3', '9-5', '900', '9000', '9-2X'],
        'Hummer': ['H1', 'H2', 'H3', 'Hummer EV', 'Hummer HX'],
        'Geely': ['Emgrand', 'Atlas', 'Boyue', 'Vision', 'Vision SUV'],
        'Chery': ['Tiggo', 'Arrizo', 'Fulwin', 'QQ', 'Tiggo 8'],
        'BYD': ['Tang', 'Qin', 'Han', 'Song', 'Yuan'],
        'Mahindra': ['Thar', 'Scorpio', 'XUV500', 'Marazzo', 'Bolero'],
        'Tata Motors': ['Nano', 'Indica', 'Tiago', 'Tigor', 'Harrier']
    }

    # Erstelle Autoeinträge basierend auf echten Modellen
    auto_entries = []
    for hersteller_index, manufacturer in enumerate(manufacturers, start=1):
        for model in models_dict.get(manufacturer, []):
            jahr = random.randint(2015, 2023)
            price = random.randint(15000, 100000)
            auto_entries.append((model, jahr, price, hersteller_index))

    cursor.executemany(
        "INSERT INTO autos (model, jahr, price, hersteller_id) VALUES (?, ?, ?, ?)",
        auto_entries
    )

    # Anbieter (Verkäufer)
    vendor_names = [
        "Habert", "Bernard", "Albert", "Maria", "Pannyellow",
        "Dejan", "Adem", "Dmytro", "Dio", "Magdalena", "Roman", "Alexander"
    ]
    cursor.executemany("INSERT INTO anbieter (name) VALUES (?)", [(v,) for v in vendor_names])

    # Für jedes Auto werden 3 bis 4 Angebote generiert.
    angebot_entries = []
    for auto_index, (model, jahr, base_price, hersteller_id) in enumerate(auto_entries, start=1):
        number_of_offers = random.choice([3, 4])
        for j in range(number_of_offers):
            vendor_index = (auto_index + j - 1) % len(vendor_names)
            vendor_id = vendor_index + 1
            manufacturer = manufacturers[hersteller_id - 1]
            variations = [0.95, 1.0, 1.05, 1.1]
            variation = variations[j % len(variations)]
            angebot_preis = int(base_price * variation)
            angebot_preis = (angebot_preis // 100) * 100  # ergibt 17500

            beschreibung = (
                f"{vendor_names[vendor_index]} bietet einen {manufacturer} {model} "
                f"({jahr}) an. Basispreis: {base_price}, Angebotspreis: {angebot_preis}"
            )
            angebot_entries.append((angebot_preis, beschreibung, auto_index, vendor_id))

    cursor.executemany(
        "INSERT INTO angebot (angebot_preis, beschreibung, auto_id, anbieter_id) VALUES (?, ?, ?, ?)",
        angebot_entries
    )
    cursor.execute("""
    INSERT INTO users (username, password) VALUES ('admin', 'Password'),
    ('Magdalena', 'Password'),
    ('guest', 'Password'),
    ('Adem', 'Password'),
    ('Dmytro', 'Password'),
    ('Dionys', 'Password'),
    ('Dejan', 'Password'),
    ('Alexander', 'Password') 
    """)

    connection.commit()
    connection.close()
    print("Datensätze erstellt")


# -------------------------------
# -------------------------- RUN
# -------------------------------
create()
add_insert()
