from flask import Flask, render_template, request, redirect, session
import psycopg2

app = Flask(__name__)
app.secret_key = '51f8d776151eb684f7b50e1ad0d31210c8178950b615f061'  


def get_db_connection():
    connection = psycopg2.connect(
        database="dali",
        user="postgres",
        password="roua",
        host="localhost",
        port="5432"
    )
    return connection

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Query to check if the user exists
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        
        cursor.close()
        connection.close()

        if user:
            # If user exists, store their email in session
            session['email'] = email
            return redirect('/dashboard')  # Redirect to dashboard or any other page
        else:
            return render_template('login.html', message='Invalid email or password! Try again ')

    return render_template('login.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        # If user is logged in, render dashboard
        return render_template('dashboard.html', email=session['email'])
    else:
        # If user is not logged in, redirect to login page
        return redirect('/login')

# Logout route
@app.route('/logout')
def logout():
    session.pop('email', None)  # Remove email from session
    return render_template('logout.html') # Redirect to login pageredirect('/logout')  

@app.route('/')
def index():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
