#--------------------------------------------------------------------
# Importamos el framework Flask
from flask import Flask

# Importamos la función que nos permit el render de los templates,
# recibir datos del form, redireccionar, etc.
from flask import render_template, request,redirect, send_from_directory, flash

# Importamos el módulo que permite conectarnos a la BS
from flaskext.mysql import MySQL

# Importamos las funciones relativas a fecha y hora
from datetime import datetime

# Importamos paquetes de interfaz con el sistema operativo.
import os
#--------------------------------------------------------------------


# Creamos la aplicación
app = Flask(__name__)

#--------------------------------------------------------------------
# Creamos la conexión con la base de datos:
mysql = MySQL()
# Creamos la referencia al host, para que se conecte a la base
# de datos MYSQL utilizamos el host localhost
app.config['MYSQL_DATABASE_HOST']='localhost'
# Indicamos el usuario, por defecto es user
app.config['MYSQL_DATABASE_USER']='root'
# Sin contraseña, se puede omitir
app.config['MYSQL_DATABASE_PASSWORD']=''
# Nombre de nuestra BD
app.config['MYSQL_DATABASE_BD']='yamaha'
# Creamos la conexión con los datos
mysql.init_app(app)
#--------------------------------------------------------------------

#--------------------------------------------------------------------
# Guardamos la ruta de la carpeta "uploads" en nuestra app
CARPETA = os.path.join('uploads')
app.config['CARPETA']=CARPETA


#--------------------------------------------------------------------
# Generamos el acceso a la carpeta uploads.
# El método uploads que creamos nos dirige a la carpeta (variable CARPETA)
# y nos muestra la foto guardada en la variable nombreFoto.
@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'], nombreFoto)

# Proporcionamos la ruta a la raiz del sitio
@app.route('/')
def index():
    # Creamos una variable que va a contener la consulta sql:
    sql = "SELECT * FROM `yamaha`.`stock`;"

    # Nos conectamos a la base de datos
    conn = mysql.connect()

    # Sobre el cursor vamos a realizar las operaciones
    cursor = conn.cursor()

    # Ejecutamos la sentencia SQL sobre el cursor
    cursor.execute(sql)

    # Copiamos el contenido del cursor a una variable
    db_stock = cursor.fetchall()

    # "Commiteamos" (Cerramos la conexión)
    conn.commit()

    # Devolvemos código HTML para ser renderizado
    return render_template('stock/index.html', stock = db_stock)

@app.route('/inventario')
def inventario():
    # Creamos una variable que va a contener la consulta sql:
    sql = "SELECT * FROM `yamaha`.`stock`;"

    # Nos conectamos a la base de datos
    conn = mysql.connect()

    # Sobre el cursor vamos a realizar las operaciones
    cursor = conn.cursor()

    # Ejecutamos la sentencia SQL sobre el cursor
    cursor.execute(sql)

    # Copiamos el contenido del cursor a una variable
    db_stock = cursor.fetchall()

    # "Commiteamos" (Cerramos la conexión)
    conn.commit()

    # Devolvemos código HTML para ser renderizado
    return render_template('stock/inventario.html', stock = db_stock)

@app.route('/motos')
def motos():
    return render_template('stock/motos.html')

@app.route('/agencias')
def agencias():
    return render_template('stock/agencias.html')

@app.route('/historia')
def historia():
    return render_template('stock/historia.html')

@app.route('/contacto')
def contacto():
    return render_template('stock/contacto.html')
#--------------------------------------------------------------------
# Función para eliminar un registro
@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM `yamaha`.`stock` WHERE id=%s", (id))
    conn.commit()
    return render_template('stock/index.html')

#--------------------------------------------------------------------
# Función para crear un registro nuevo.
@app.route('/carga')
def create():
    return render_template('stock/carga.html')

#--------------------------------------------------------------------
#Función para almacenar los datos de un usuario.
@app.route('/store', methods=['POST'])
def storage():
    # Recibimos los valores del formulario y los pasamos a variables locales:
    _modelo = request.form['modelo']
    _color = request.form['color']
    _motor = request.form['motor']
    _chasis = request.form['chasis']
    _cc = request.form['cc']
    _foto = request.files['foto']

    # Guardamos en now los datos de fecha y hora
    now = datetime.now()

    # Y en tiempo almacenamos una cadena con esos datos
    tiempo = now.strftime("%Y%H%M%S")

    #Si el nombre de la foto ha sido proporcionado en el form...
    if _foto.filename!='':
        #...le cambiamos el nombre.
        nuevoNombreFoto=tiempo+_foto.filename
        # Guardamos la foto en la carpeta uploads.
        _foto.save("uploads/"+nuevoNombreFoto)

    # Y armamos una tupla con esos valores:
    datos = (_modelo,_color,_motor,_chasis,_cc, nuevoNombreFoto)

    # Armamos la sentencia SQL que va a almacenar estos datos en la DB:
    sql = "INSERT INTO `yamaha`.`stock` \
    (`id`, `modelo`, `color`, `motor`, `chasis`, `cilindrada`, `foto`) \
    VALUES (NULL, %s, %s, %s, %s, %s, %s);"

    conn = mysql.connect()     # Nos conectamos a la base de datos
    cursor = conn.cursor()     # En cursor vamos a realizar las operaciones
    cursor.execute(sql, datos) # Ejecutamos la sentencia SQL en el cursor
    conn.commit()              # Hacemos el commit
    return render_template('stock/index.html') # Volvemos a index.html

@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `yamaha`.`stock` WHERE id=%s", (id))
    stock=cursor.fetchall()
    conn.commit()
    return render_template('stock/edit.html', stock=stock)

@app.route('/update', methods=['POST'])
def update():
    # Recibimos los valores del formulario y los pasamos a variables locales:
    _modelo = request.form['modelo']
    _color = request.form['color']
    _motor = request.form['motor']
    _chasis = request.form['chasis']
    _cc = request.form['cc']
    _foto = request.files['foto']
    id = request.form['id']

    # Armamos la sentencia SQL que va a actualizar los datos en la DB:
    sql = "UPDATE `yamaha`.`stock` SET `modelo`=%s, `color`=%s, `motor`=%s, `chasis`=%s, `cilindrada`=%s WHERE id=%s;"
    # Y la tupla correspondiente
    datos = (_modelo,_color,_motor,_chasis,_cc,id)

    conn = mysql.connect()
    cursor = conn.cursor()

    # Guardamos en now los datos de fecha y hora
    now = datetime.now()

    # Y en tiempo almacenamos una cadena con esos datos
    tiempo= now.strftime("%Y%H%M%S")

    #Si el nombre de la foto ha sido proporcionado en el form...
    if _foto.filename != '':
        # Creamos el nombre de la foto y la guardamos.
        nuevoNombreFoto = tiempo + _foto.filename
        _foto.save("uploads/" + nuevoNombreFoto)

        # Buscamos el registro y buscamos el nombre de la foto vieja:
        cursor.execute("SELECT foto FROM `yamaha`.`stock` WHERE id=%s", id)
        fila= cursor.fetchall()

        # Y la borramos de la carpeta:
        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))

        # Finalmente, actualizamos la DB con el nuevo nombre del archivo:
        cursor.execute("UPDATE `yamaha`.`stock` SET foto=%s WHERE id=%s;", (nuevoNombreFoto, id))
        conn.commit()

    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/')



#--------------------------------------------------------------------
# Estas líneas de código las requiere python para que
# se pueda empezar a trabajar con la aplicación
if __name__=='__main__':
    #Corremos la aplicación en modo debug
    app.run(debug=True)
#--------------------------------------------------------------------