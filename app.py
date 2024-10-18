from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Simulación de verificación (debería reemplazarse por verificación en base de datos)
        if username == "admin" and password == "password":
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('login_success'))
        else:
            return redirect(url_for('login_fail'))
    
    return render_template('index.html')

@app.route('/login-success')
def login_success():
    return render_template('login_success.html', username=session.get('username'))

@app.route('/login-fail')
def login_fail():
    return render_template('login_fail.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)