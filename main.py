from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import sqlite3

# Flask App Initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SuperSecret'

# Flask-Login Initialization
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Bitte loggen Sie sich ein, um diese Seite zu sehen.'

# Konstanten für die dbcurso Funktion
QUERY_TYPE_ALL = 1  # gibt eine Liste von allen Zeilen aus Select aus
QUERY_TYPE_ONE = 0  # gibts nur eine Zeile aus Select


# --- HELPER FUNCTIONS ---
# --- dbcursor macht connect / cursor / execute / commit und close, dadurch sparen wir uns das ständige wiederholen
def dbcursor(query, params=None, fetch_type=None):
    try:
        connection = sqlite3.connect('data/autowelt.db')
        cursor = connection.cursor()
        # Execute query
        cursor.execute(query, params or ())
        if fetch_type == QUERY_TYPE_ALL:
            result = cursor.fetchall()
        else:
            result = cursor.fetchone()
        connection.commit()
    finally:
        connection.close()
    return result


def ganze_tabelle(table_name):
    return dbcursor(f"SELECT * FROM {table_name}", fetch_type=QUERY_TYPE_ALL)


# --- USER MODEL AND AUTHENTICATION --- KI generiert für das Usermodel
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username


@login_manager.user_loader
def load_user(user_id):
    user_data = dbcursor("SELECT id, username FROM users WHERE id = ?", (user_id,), QUERY_TYPE_ONE)
    return User(user_data[0], user_data[1])


# --- ROUTES --- bzw Views
@app.route('/')
def startseite():
    username = current_user.username if current_user.is_authenticated else None
    return render_template('startseite.html', username=username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Verify user credentials
        user_data = dbcursor("SELECT id, username, password FROM users WHERE username = ? AND password = ?",
                             (username, password), QUERY_TYPE_ONE)

        if user_data:
            login_user(User(user_data[0], user_data[1]))  # Log the user in
            return redirect(url_for('startseite'))  # Redirect to homepage
        return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()  # Logout current user
    return redirect(url_for('startseite'))


@app.route('/suche')
def suche():
    hersteller_list = ganze_tabelle("hersteller")
    return render_template("suche.html", data=hersteller_list)


@app.route('/suchergebnis', methods=['GET'])
def suchergbebnis():
    hersteller_id = request.args.get('id')
    query = """
        SELECT hersteller.id, hersteller.name, autos.model, autos.jahr, autos.price, 
               anbieter.name, angebot.angebot_preis, angebot.beschreibung
        FROM hersteller 
        JOIN autos ON hersteller.id = autos.hersteller_id 
        JOIN angebot ON angebot.auto_id = autos.id 
        JOIN anbieter ON angebot.anbieter_id = anbieter.id 
        WHERE hersteller.id = ?
    """
    suchergebnisse = dbcursor(query, (hersteller_id,), QUERY_TYPE_ALL)
    return render_template('suche-ergebnisse.html', data=suchergebnisse)


@app.route('/angebot_erstellen', methods=['GET', 'POST'])
@login_required  # benötigt login für den view!
def angebot_erstellen():
    if request.method == 'POST':
        automodel_name = request.form.get('automodel')
        preis = request.form.get('preis')
        beschreibung = request.form.get('beschreibung')
        query = """
            INSERT INTO angebot (angebot_preis, beschreibung, auto_id, anbieter_id)
            VALUES (
                ?, ?, 
                (SELECT id FROM autos WHERE model = ?), 
                (SELECT id FROM anbieter WHERE name = ?)
            )
        """
        dbcursor(query, (preis, beschreibung, automodel_name, current_user.username))
        return redirect(url_for('erfolgreich_eingefuegt'))

    hersteller_list = ganze_tabelle("hersteller")
    autos_list = ganze_tabelle("autos")
    anbieter_list = ganze_tabelle("anbieter")
    return render_template(
        'angebot-erstellen.html',
        hersteller_liste=hersteller_list,
        modelle_liste=autos_list,
        verkaeufer_liste=anbieter_list,
    )


@app.route('/erfolgreich-eingefuegt', methods=['GET'])
def erfolgreich_eingefuegt():
    return render_template('erfolgreich-eingefuegt.html', bodyclass="AngebotErstellt")


@app.route('/users')
def users():
    user_rows = ganze_tabelle("users")
    return render_template("benutzer.html", rows=user_rows)


# --- Starte als Main nur, wenn die Datei direkt ausgeführt wird
if __name__ == '__main__':
    app.run(debug=True)
