from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import bcrypt

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
        return connection
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None

def verify_user(connection, username, password):
    try:
        select_query = "SELECT password_hash, rol FROM users WHERE username = %s"
        cursor = connection.cursor()
        cursor.execute(select_query, (username,))
        result = cursor.fetchone()

        if result:
            stored_password_hash, role = result
            if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
                print(f"Inicio de sesión exitoso para el usuario '{username}' con rol '{role}'")
                return role  # Retorna el rol en caso de éxito
            else:
                print("Contraseña incorrecta")
                return None
        else:
            print(f"Usuario '{username}' no encontrado")
            return None
    except mysql.connector.Error as e:
        print(f"Error al verificar usuario: {e}")
        return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = create_connection()
        if conn:
            role = verify_user(conn, username, password)
            conn.close()
            if role:
                session['logged_in'] = True
                session['username'] = username
                session['role'] = role
                # Redirige según el rol del usuario
                if role == 'admin':
                    return redirect(url_for('admin_page'))
                else:
                    return redirect(url_for('user_page'))
            else:
                flash('Nombre de usuario o contraseña incorrecta', 'danger')
    
    return render_template('index.html')

@app.route('/admin')
def admin_page():
    if session.get('logged_in') and session.get('role') == 'admin':
        return render_template('login_success.html', username=session['username'], is_admin=True)
    else:
        return redirect(url_for('login'))

@app.route('/user')
def user_page():
    if session.get('logged_in') and session.get('role') == 'user':
        return render_template('login_success.html', username=session['username'], is_admin=False)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    conn = create_connection()
    if conn:
        conn.close()
    app.run(debug=True)
