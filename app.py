# app.py - Main Flask Application

from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from model.predict import get_recommendations

app = Flask(__name__)
app.secret_key = 'career_secret_key_2025'

# ------------------------------------------------------------------
# MySQL Configuration — update with your credentials
# ------------------------------------------------------------------
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root123',  # ← change this
    'database': 'career_db'
}


def get_db():
    return mysql.connector.connect(**DB_CONFIG)


# ------------------------------------------------------------------
# ROUTES
# ------------------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        name     = request.form['name']
        email    = request.form['email']
        password = request.form['password']
        gpa      = float(request.form['gpa'])

        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO users (name, email, password, gpa) VALUES (%s, %s, %s, %s)",
                (name, email, password, gpa)
            )
            db.commit()
            user_id = cursor.lastrowid
            session['user_id'] = user_id
            session['user_name'] = name
            db.close()
            return redirect(url_for('profile'))
        except mysql.connector.IntegrityError:
            error = "Email already registered. Please login."

    return render_template('register.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email    = request.form['email']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        db.close()

        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            return redirect(url_for('profile'))
        else:
            error = "Invalid email or password."

    return render_template('login.html', error=error)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        user_id        = session['user_id']
        python_skill   = int(request.form['python_skill'])
        ml_skill       = int(request.form['ml_skill'])
        web_skill      = int(request.form['web_skill'])
        database_skill = int(request.form['database_skill'])
        aptitude_score = int(request.form['aptitude_score'])
        interest       = request.form['interest']

        # Get GPA from DB
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT gpa FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()
        gpa = user['gpa']

        # Save profile (convert all to native Python types for MySQL)
        cursor.execute("""
            INSERT INTO user_profiles
            (user_id, python_skill, ml_skill, web_skill, database_skill, aptitude_score, interest)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (int(user_id), int(python_skill), int(ml_skill), int(web_skill), int(database_skill), int(aptitude_score), str(interest)))
        db.commit()

        # Get ML recommendations
        results, gaps = get_recommendations(
            python_skill, ml_skill, web_skill, database_skill, aptitude_score, gpa
        )

        # Save top recommendation to DB
        if results:
            top = results[0]
            cursor.execute("""
                INSERT INTO recommendations (user_id, career_role, match_score, demand_level)
                VALUES (%s,%s,%s,%s)
            """, (int(user_id), str(top['career_role']), float(top['match_score']), str(top['demand'])))
            db.commit()

        db.close()

        # Store in session for results page
        session['results'] = results
        session['gaps']    = gaps
        return redirect(url_for('result'))

    return render_template('profile.html', user_name=session.get('user_name'))


@app.route('/result')
def result():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    results = session.get('results', [])
    gaps    = session.get('gaps', [])
    return render_template('result.html',
                           user_name=session.get('user_name'),
                           results=results,
                           gaps=gaps)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# ------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)