
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
#from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'beispiel'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Connect to the database
        connection = sqlite3.connect('autowelt.db')
        cursor = connection.cursor()

        # Query the database for the user
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()  # Fetch one user record

        connection.close()

        if user:
            session['logged_in'] = True
            session['username'] = username  # Store the username in the session
            return redirect(url_for('homepage'))  # Redirect to homepage
        else:
            return render_template('login.html', error="Ungültige Anmeldedaten")  # Show login page with error message

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('homepage'))
   # return render_template('HOMEPAGE.html')
@app.route('/search')
def angebot_suchen():
    # Verbindung zur Datenbank herstellen
    connection = sqlite3.connect('autowelt.db')
    cursor = connection.cursor()
    # SQL-Abfrage ausführen: Annahme, dass die Tabelle "hersteller" die Spalten "id" und "name" enthält
    query = cursor.execute("SELECT id, name FROM hersteller")
    hersteller_liste = query.fetchall()  # Liefert eine Liste von Zeilen (sqlite3.Row-Objekte)
    print(hersteller_liste)
    connection.close()
    return render_template("searchOffers.html", data=hersteller_liste)
@app.route('/result', methods=['GET'])
def show_data():
    hersteller_id = request.args.get('id')
    print(hersteller_id)
    connection = sqlite3.connect('autowelt.db')
    cursor = connection.cursor()
    cursor.execute(f"""
    SELECT hersteller.id, hersteller.name, autos.model, autos.jahr, autos.price, 
           anbieter.name, angebot.angebot_preis, angebot.beschreibung
    FROM hersteller 
    JOIN autos ON hersteller.id = autos.hersteller_id 
    JOIN angebot ON angebot.auto_id = autos.id 
    JOIN anbieter ON angebot.anbieter_id = anbieter.id 
    WHERE hersteller.id = ?
    """,(hersteller_id,))
    rows = cursor.fetchall()
    connection.close()
    return render_template('results.html', data=rows)
@app.route('/angebot_erstellen', methods=['GET'])
def angebot_erstellen():
    connection = sqlite3.connect('autowelt.db')
    cursor = connection.cursor()
    username = session.get('username')
    cursor.execute("Select * FROM hersteller")
    hersteller = cursor.fetchall()
    cursor.execute("Select * FROM autos")
    modelle = cursor.fetchall()
    cursor.execute("Select * FROM anbieter")
    verkaufer = cursor.fetchall()
    connection.close()
    return render_template('createOffer.html', hersteller_liste=hersteller, modelle_liste=modelle, verkaeufer_liste=verkaufer, username=username)


# ?hersteller=Volkswagen&automodel=M3&preis=1234&beschreibung=Hallo+Dejan&verkaeufer=Bernard
@app.route('/angebot_einfuegen', methods=['GET'])
def angebot_einfuegen():
    connection = sqlite3.connect('autowelt.db')
    cursor = connection.cursor()
    username= session.get('username')
    hersteller_name = request.args.get('hersteller')
    automodel_name = request.args.get('automodel')
    preis = request.args.get('preis')
    beschreibung = request.args.get('beschreibung')
    anbieter = username
    print(anbieter)
    print("-------------------------")
    cursor.execute(
        "INSERT INTO angebot (angebot_preis, beschreibung, auto_id, anbieter_id) VALUES (?, ?, (SELECT id FROM autos WHERE model = ?), (SELECT id FROM anbieter WHERE name = ?))",
        (preis, beschreibung, automodel_name, anbieter)
    )
    connection.commit()
    connection.close()

    # DEBUG
    print(hersteller_name, automodel_name, preis, beschreibung, anbieter)
    return render_template('angeboterstellt.html')
@app.route('/', methods=['GET'])
def homepage():
    username = session.get('username',"Gast")
    return render_template('HOMEPAGE.html', username=username)

@app.route('/users')
def users():
    connection = sqlite3.connect('autowelt.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()  # Liefert eine Liste von Zeilen (sqlite3.Row-Objekte)

    connection.close()

    return render_template("users.html", rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
