from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import bcrypt

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Datos de conexión a la base de datos
DB_HOST = "b4axyho3yrtcor1vlcof-mysql.services.clever-cloud.com"
DB_NAME = "b4axyho3yrtcor1vlcof"
DB_USER = "umppnjai4hpsfxb3"
DB_PASSWORD = "C2NQx1PpyVlWOjVuxPoC"
DB_PORT = 3306

# Función para crear la conexión a la base de datos
def create_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Ruta principal para el formulario de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = create_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT username, password_hash FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                flash('Inicio de sesión exitoso', 'success')
                return redirect(url_for('login'))
            else:
                flash('Nombre de usuario o contraseña incorrectos', 'danger')
        else:
            flash('Error en la conexión a la base de datos', 'danger')
    
    return render_template('login.html')

# Ruta de registro (puedes implementarla)
@app.route('/register', methods=['GET', 'POST'])
def register():
    return "Página de registro en construcción"

if __name__ == '__main__':
    app.run(debug=True)