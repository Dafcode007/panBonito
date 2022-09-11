from datetime import timedelta
from flask import Flask, flash, g, request, redirect, session, render_template, url_for
from flask_mysqldb import MySQL
from backend.orm import ConexionDB


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'mysql.perseoq.party'
app.config['MYSQL_USER'] = 'superanet'
app.config['MYSQL_PASSWORD'] = 'the37855'
app.config['MYSQL_DB'] = 'panbonito'


app.secret_key ='000'
MySQL(app)
db = ConexionDB()

@app.before_request
def before():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=10)
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/')
def index():
    return render_template('login/login.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user', None)
        if request.method == 'POST':
            username = request.form['form_user'] 
            passwd = request.form['form_passwd']
            query = f'SELECT * FROM users WHERE usuario="{username}" and clave="{passwd}" '
            datos = db.fetch(query)
            if datos:
                session['user'] = request.form['form_user']
                return redirect(url_for('principal'))
            return redirect(url_for('index'))
        return redirect(url_for('index'))
    return render_template('login/login.html')

@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/home')
def principal():
    if g.user:
        return render_template('login/principal.html', user=session['user'])
    return redirect(url_for('index'))

# PAN BONITO BACKEND

@app.route('/agregar_producto', methods=['GET','POST'])
def add_bread():
    if g.user:
        if request.method=='POST':
            bread = request.form['nombre_pan']
            exist = request.form['existencias']
            price = request.form['precio']
            query = f'INSERT INTO inventario(pan, existencia, precio) VALUES("{bread}","{exist}","{price}")'
            db.save(query)
            return redirect(url_for('show_bread', user=session['user']))
        return render_template('inventario/agregar_existencias.html', user=session['user'])
    return redirect(url_for('index'))

@app.route('/inventario')
def show_bread():
    if g.user:
        query = 'SELECT * FROM inventario'
        datos = db.fetch(query)
        return render_template('inventario/existencias.html', datos=datos, user=session['user'])
    return redirect(url_for('index'))

@app.route('/ventas')
def ventas():
    if g.user:
        query = 'select * from inventario'
        datos = db.fetch(query) # Listamos el inventario 
        return render_template('ventas/ventas.html', user=session['user'], productos=datos)
    return redirect(url_for('index'))

@app.route('/ventas/action', methods=['GET', 'POST'])
def action_ventas():
    if g.user:
        if request.method == 'POST':
            producto_seleccionado = request.form['lista_productos']
            cantidad_pan = request.form['cantidad']
            ex = f'SELECT existencia FROM inventario WHERE id_inventario="{producto_seleccionado}"'
            get_ex = db.fetch(ex) # Donas de Chocoate, existencias 100 piezas = ((100,),)s
            element = [i[0] for i in get_ex] # Convertimos a lista el resultado de get_ex
            existencias = element[0] # extraemos el numero de la lista
            if  existencias > 0: 
                cantidad_actualizada = existencias - int(cantidad_pan)
                query = f'UPDATE inventario SET existencia="{cantidad_actualizada}" WHERE id_inventario="{producto_seleccionado}"'
                db.save(query)
                return redirect(url_for('show_bread', user=session['user']))
            else:
                flash('No hay existencias')
        return redirect(url_for('ventas', user=session['user']))
    return redirect(url_for('index'))

@app.route('/carrito_de_compras')
def carrito():
    pass # Posible solución en https://www.youtube.com/watch?v=5vTZgIQ0aSg

if __name__ == '__main__':
    app.run(debug=True)
