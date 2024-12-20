# Importamos las herramientas que necesitamos para crear nuestra aplicación web
from flask import Flask, render_template, request, redirect
# Importamos la herramienta para trabajar con bases de datos
from flask_sqlalchemy import SQLAlchemy

# Creamos nuestra aplicación web
app = Flask(__name__)
# Le decimos a nuestra aplicación que usaremos una base de datos llamada 'diary.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
# Desactivamos una característica que no necesitamos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Conectamos nuestra aplicación a la base de datos
db = SQLAlchemy(app)

# Creamos una clase llamada 'Card' que representa una tabla en nuestra base de datos
class Card(db.Model):
    # Creamos una columna llamada 'id' que será el identificador único de cada tarjeta
    id = db.Column(db.Integer, primary_key=True)
    # Creamos una columna para el título de la tarjeta
    title = db.Column(db.String(100), nullable=False)
    # Creamos una columna para la descripción de la tarjeta
    subtitle = db.Column(db.String(300), nullable=False)
    # Creamos una columna para el texto de la tarjeta
    text = db.Column(db.Text, nullable=False)

    # Esta función nos ayuda a ver información sobre la tarjeta cuando la imprimimos
    def __repr__(self):
        return f'<Card {self.id}>'

# Creamos una clase llamada 'User' que representa una tabla de usuarios en nuestra base de datos
class User(db.Model):
    # Creamos una columna llamada 'id' que será el identificador único de cada usuario
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Creamos una columna para el nombre de usuario
    login = db.Column(db.String(100), nullable=False)
    # Creamos una columna para la contraseña del usuario
    password = db.Column(db.String(30), nullable=False)

# Creamos una ruta para la página de inicio de sesión
@app.route('/', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        # Obtenemos el nombre de usuario y la contraseña del formulario
        form_login = request.form['email']
        form_password = request.form['password']
        
        # Buscamos todos los usuarios en la base de datos
        users_db = User.query.all()
        for user in users_db:
            # Comprobamos si el nombre de usuario y la contraseña son correctos
            if form_login == user.login and form_password == user.password:
                return redirect('/index')
        else:
            # Si no son correctos, mostramos un mensaje de error
            error = 'Nombre de usuario o contraseña incorrectos'
        return render_template('login.html', error=error)
    else:
        return render_template('login.html')

# Creamos una ruta para la página de registro
@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        # Obtenemos el nombre de usuario y la contraseña del formulario
        login = request.form['email']
        password = request.form['password']
        
        # Creamos un nuevo usuario y lo guardamos en la base de datos
        user = User(login=login, password=password)
        db.session.add(user)
        db.session.commit()
        
        return redirect('/')
    else:
        return render_template('registration.html')

# Creamos una ruta para la página principal
@app.route('/index')
def index():
    # Obtenemos todas las tarjetas de la base de datos y las mostramos en la página
    cards = Card.query.order_by(Card.id).all()
    return render_template('index.html', cards=cards)

# Creamos una ruta para ver una tarjeta específica
@app.route('/card/<int:id>')
def card(id):
    # Obtenemos la tarjeta con el id especificado y la mostramos en la página
    card = Card.query.get(id)
    return render_template('card.html', card=card)

# Creamos una ruta para la página de creación de tarjetas
@app.route('/create')
def create():
    return render_template('create_card.html')

# Creamos una ruta para manejar el formulario de creación de tarjetas
@app.route('/form_create', methods=['GET', 'POST'])
def form_create():
    if request.method == 'POST':
        # Obtenemos los datos del formulario
        title = request.form['title']
        subtitle = request.form['subtitle']
        text = request.form['text']

        # Creamos una nueva tarjeta y la guardamos en la base de datos
        card = Card(title=title, subtitle=subtitle, text=text)
        db.session.add(card)
        db.session.commit()
        return redirect('/index')
    else:
        return render_template('create_card.html')

# Iniciamos nuestra aplicación web
if __name__ == "__main__":
    app.run(debug=True)