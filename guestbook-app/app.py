from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'guestbook.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Invitado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    invitados = Invitado.query.all()
    return render_template('index.html', invitados=invitados)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form.get('nombre')
    mensaje = request.form.get('mensaje')

    if not nombre or not mensaje:
        return "Faltan datos", 400

    nuevo = Invitado(nombre=nombre, mensaje=mensaje)
    db.session.add(nuevo)
    db.session.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)