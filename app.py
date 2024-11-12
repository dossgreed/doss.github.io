from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import bcrypt

#app = Flask(__name__)
app = Flask(__name__, template_folder='templates')
app.secret_key = "your_secret_key"  # Cambia esto por una clave secreta segura

# Datos de conexión a la base de datos
DB_HOST = "b4axyho3yrtcor1vlcof-mysql.services.clever-cloud.com"
DB_NAME = "b4axyho3yrtcor1vlcof"
DB_USER = "umppnjai4hpsfxb3"
DB_PASSWORD = "C2NQx1PpyVlWOjVuxPoC"
DB_PORT = 3306

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        if connection.is_connected():
            print("Conexión exitosa a la base de datos.")
            # Prueba con una consulta simple para confirmar la conexión.
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()
            print(f"Conectado a la base de datos: {db_name[0]}")
            cursor.close()
        return connection
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None

def verify_user(connection, username, password):
    try:
        select_query = "SELECT password_hash FROM users WHERE username = %s"
        cursor = connection.cursor()
        cursor.execute(select_query, (username,))
        result = cursor.fetchone()

        if result:
            stored_password_hash = result[0]
            if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
                print(f"Inicio de sesión exitoso para el usuario '{username}'")
                return True
            else:
                print("Contraseña incorrecta")
                return False
        else:
            print(f"Usuario '{username}' no encontrado")
            return False
    except Error as e:
        print(f"Error al verificar usuario: {e}")
        return False

# Ruta principal para el formulario de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

         # Usar flash para mostrar los valores en la interfaz
        

        # Redirigir a la misma página para ver los mensajes flash
    #return redirect(url_for('show_data', username=username, password=password))
        
        conn = create_connection()
        if conn:
            if verify_user(conn, username, password):
                session['logged_in'] = True
                session['username'] = username
                conn.close()
                return redirect(url_for('login_success'))
            else:
                conn.close()
                flash('Nombre de usuario y contraseña incorrecta', 'danger')
                #return redirect(url_for('login_fail'))
                #flash(f"Recibido username: {session['logged_in']}")
                #flash(f"Recibido password: {session['username']}")
                #return redirect(url_for('show_data', username=session['username'], password=session['logged_in']))
    
    return render_template('index.html')

# Ruta para la página de éxito de inicio de sesión
#
@app.route('/login-success')
def login_success():
    if session.get('logged_in'):
       return render_template('login_success.html', username=session.get('username'))
    else:
        return redirect(url_for('login'))

# Ruta para la página de fallo en el inicio de sesión
@app.route('/login-fail')
def login_fail():
    return render_template('login_fail.html')

 #Ruta de cierre de sesión
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/show-data')
def show_data():
    username = request.args.get('username')
    password = request.args.get('password')
    return render_template('show_data.html', username=username, password=password)

if __name__ == '__main__':
    conn = create_connection()
    if conn:
        conn.close()
    app.run(debug=True)