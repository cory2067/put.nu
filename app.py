from flask import Flask, abort, send_from_directory, redirect, render_template, url_for, flash, request, jsonify
import flask_login
import os
import sqlite3 # If we get a real user base we should migrate to Postgres.
from passlib.hash import pbkdf2_sha256


app = Flask(__name__)
# TODO: before release change secret key to an environment variable (and different value)
app.config['SECRET_KEY'] = '\x9d\xbc]\xda\xda\x94\x9fs\x8f\x1b)#\xa8C\xecW\xfdC,%v\x1e\x0f\xd7'

STORAGE_PATH = 'files'

# Login manager init
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
	pass

@login_manager.user_loader
def user_loader(username):
	user = User()
	user.id = username
	return user

def logged_in():
	if not flask_login.current_user.is_anonymous:
		return True
	return False


# DB init
conn = sqlite3.connect('putnu.db')
c = conn.cursor()
try:
	c.execute('SELECT * FROM users')
except sqlite3.OperationalError as e:
	if 'no such table: users' in str(e):
		print('Users table does not exist. Creating users table.')
		c.execute('CREATE TABLE users(username TEXT, email TEXT, password TEXT)')
		conn.commit()
	else:
		raise e
conn.close()


@app.route("/")
def index():
	print(url_for('login'))
	return render_template('index.html', logged_in=logged_in())

@app.route("/<path>")
def fetch(path):
	if not os.path.isfile(os.path.join(STORAGE_PATH, path)):
		return resolve_link(path) #if not a file, try to resolve as shortened link

	return send_from_directory(STORAGE_PATH, path)

@app.route('/account')
def account():
	if logged_in():
		return render_template('index.html', logged_in=logged_in()) # Add account page later
	return render_template('login.html')

@app.route('/create_account', methods = ['POST'])
def create_account():
	with sqlite3.connect('putnu.db') as conn:
		c = conn.cursor()
		#	email = request.form['email']
		email = '' # Not implemented yet, unclear if email will serve a function
		username = request.form['username']
		password = request.form['password']

		c.execute("SELECT username FROM users WHERE username = ?", [username])
		existing = c.fetchone();
		if existing:
			return jsonify({'success': False, 'error': '#register-user'})

		hashed_pass = pbkdf2_sha256.encrypt(password)

		c.execute('INSERT INTO users VALUES (?, ?, ?)', [username, email, hashed_pass])
		conn.commit()

		return jsonify({'success': True})

@app.route('/login', methods = ['POST'])
def login():
	with sqlite3.connect('putnu.db') as conn:
		c = conn.cursor()
		username = request.form['username']
		password = request.form['password']

		c.execute("SELECT password FROM users WHERE username = ?", [username])
		hashed_pass = c.fetchone()

		try:
			if pbkdf2_sha256.verify(password, hashed_pass[0]):
				user = User()
				user.id = username
				flask_login.login_user(user)
				return jsonify({'success': True});
			return jsonify({'success': False, 'error': "#login-password"});
		except TypeError:
			return jsonify({'success': False, 'error': "#login-user"});

@app.route('/logout')
def logout():
	flask_login.logout_user()
	flash('Logged out.')
	return redirect(url_for('index'))

def resolve_link(url): # link shortening
	shortened = {'zucc': 'https://facebook.com'} #use a real db for this
	if url in shortened:
		return redirect(shortened[url])
	abort(404)

if __name__ == "__main__":
	app.run(host='127.0.0.1', port=8000)
