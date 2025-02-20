from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

import sqlite3
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SuperSecret'
# Initialize the LoginManager
login_manager = LoginManager(app)

# Specify the login view
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

QUERY_TYPE_ALL = "all"
QUERY_TYPE_ONE = "one"


# Helper functions to remove redundancy and make things easier
def dbcursor(query, params=None, fetch_type=None):
    connection = sqlite3.connect('data/autowelt.db')
    cursor = connection.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    fetched = None
    if fetch_type == QUERY_TYPE_ALL:
        fetched = cursor.fetchall()
    elif fetch_type == QUERY_TYPE_ONE:
        fetched = cursor.fetchone()
    connection.commit()
    connection.close()
    return fetched


def get_hersteller_list():
    return dbcursor("SELECT * FROM hersteller", None, QUERY_TYPE_ALL)


def get_available_autos():
    return dbcursor("SELECT * FROM autos", None, QUERY_TYPE_ALL)


def get_available_anbieter():
    return dbcursor("SELECT * FROM anbieter", None, QUERY_TYPE_ALL)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Verify username and password
        user_data = dbcursor("SELECT id, username, password FROM users WHERE username = ? AND password = ?",
                             (username, password), QUERY_TYPE_ONE)
        if user_data:
            user = User(user_data[0], user_data[1])
            login_user(user)  # Login the user
            return redirect(url_for('startseite'))  # Redirect to the homepage
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()  # Simplified session clearing
    return redirect(url_for('startseite'))


@app.route('/suche')
def suche():
    hersteller_list = get_hersteller_list()
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
    rows = dbcursor(query, (hersteller_id,), QUERY_TYPE_ALL)
    return render_template('suche-ergebnisse.html', data=rows)


@app.route('/angebot_erstellen', methods=['GET'])
@login_required
def angebot_erstellen():
    username = current_user.username  # Get the logged-in username
    hersteller_list = get_hersteller_list()
    autos_list = get_available_autos()
    anbieter_list = get_available_anbieter()
    return render_template(
        'angebot-erstellen.html',
        hersteller_liste=hersteller_list,
        modelle_liste=autos_list,
        verkaeufer_liste=anbieter_list,
        username=username,
    )


@app.route('/erfolgreich-eingefuegt', methods=['GET'])
def erfolgreich_eingefuegt():
    username = current_user.username
    hersteller_name = request.args.get('hersteller')
    automodel_name = request.args.get('automodel')
    preis = request.args.get('preis')
    beschreibung = request.args.get('beschreibung')
    query = """
    INSERT INTO angebot (angebot_preis, beschreibung, auto_id, anbieter_id)
    VALUES (
        ?, ?, 
        (SELECT id FROM autos WHERE model = ?), 
        (SELECT id FROM anbieter WHERE name = ?)
    )
    """
    dbcursor(query, (preis, beschreibung, automodel_name, username))
    return render_template('erfolgreich-eingefuegt.html', bodyclass="AngebotErstellt")


@app.route('/', methods=['GET'])
def startseite():
    # Check if the user is authenticated
    if current_user.is_authenticated:
        username = current_user.username
    else:
        username = None  # or set a default value like "Guest"
    return render_template('startseite.html', username=username)


@app.route('/users')
def users():
    user_rows = dbcursor("SELECT * FROM users", None, QUERY_TYPE_ALL)
    return render_template("benutzer.html", rows=user_rows)


class User(UserMixin):
    # User class for Flask-Login
    def __init__(self, id, username):
        self.id = id
        self.username = username


@login_manager.user_loader
def load_user(user_id):
    user_data = dbcursor("SELECT id, username FROM users WHERE id = ?", (user_id,), QUERY_TYPE_ONE)
    if user_data:
        return User(user_data[0], user_data[1])
    return None

if __name__ == '__main__':
    app.run(debug=True)
