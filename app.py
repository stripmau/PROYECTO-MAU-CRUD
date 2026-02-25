import os
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =============================
# MODELO TENIS
# =============================
class Tenis(db.Model):
    __tablename__ = 'tenis'

    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(60), nullable=False)
    modelo = db.Column(db.String(80), nullable=False)
    talla = db.Column(db.Numeric(4,1), nullable=False)
    color = db.Column(db.String(30))
    precio = db.Column(db.Numeric(10,2), nullable=False, default=0)
    stock = db.Column(db.Integer, nullable=False, default=0)


# =============================
# LISTAR TENIS
# =============================
@app.route('/')
def index():
    tenis = Tenis.query.all()
    return render_template('index.html', tenis=tenis)


# =============================
# CREAR TENIS
# =============================
@app.route('/tenis/new', methods=['GET','POST'])
def create_tenis():
    if request.method == 'POST':
        nuevo = Tenis(
            marca=request.form['marca'],
            modelo=request.form['modelo'],
            talla=request.form['talla'],
            color=request.form['color'],
            precio=request.form['precio'],
            stock=request.form['stock']
        )

        db.session.add(nuevo)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create_tenis.html')


# =============================
# ELIMINAR TENIS
# =============================
@app.route('/tenis/delete/<int:id>')
def delete_tenis(id):
    tenis = Tenis.query.get(id)
    if tenis:
        db.session.delete(tenis)
        db.session.commit()
    return redirect(url_for('index'))


# =============================
# ACTUALIZAR TENIS
# =============================
@app.route('/tenis/update/<int:id>', methods=['GET','POST'])
def update_tenis(id):
    tenis = Tenis.query.get(id)

    if request.method == 'POST':
        tenis.marca = request.form['marca']
        tenis.modelo = request.form['modelo']
        tenis.talla = request.form['talla']
        tenis.color = request.form['color']
        tenis.precio = request.form['precio']
        tenis.stock = request.form['stock']

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('update_tenis.html', tenis=tenis)


if __name__ == '__main__':
    app.run(debug=True)