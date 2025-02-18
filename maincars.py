from crypt import methods

from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
app = Flask(__name__)
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
@app.route('/angebot_erstellen')
def angebot_erstellen():
    connection = sqlite3.connect('autowelt.db')
    cursor = connection.cursor()
    cursor.execute("Select * FROM hersteller")
    hersteller = cursor.fetchall()
    cursor.execute("Select * FROM autos")
    modelle = cursor.fetchall()
    cursor.execute("Select * FROM anbieter")
    verkaufer = cursor.fetchall()
    connection.close()
    return render_template('createOffer.html', hersteller_liste=hersteller, modelle_liste=modelle, verkaeufer_liste=verkaufer)


# ?hersteller=Volkswagen&automodel=M3&preis=1234&beschreibung=Hallo+Dejan&verkaeufer=Bernard
@app.route('/angebot_einfuegen', methods=['GET'])
def angebot_einfuegen():
    hersteller_name = request.args.get('hersteller')
    automodel_name = request.args.get('automodel')
    preis = request.args.get('preis')
    beschreibung = request.args.get('beschreibung')
    verkaufer_name = request.args.get('verkaufer')
    print(hersteller_name, automodel_name, preis, beschreibung, verkaufer_name)
    return "Ihr Angebot wurde erfolgreich erstellt"
@app.route('/')
def homepage():
    return render_template('HOMEPAGE.html')

if __name__ == '__main__':
    app.run(debug=True)
