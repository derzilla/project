from flask import Flask, render_template, request, redirect, url_for, make_response
import sqlite3
import requests


app = Flask(__name__)


@app.route('/')

def main():

	return render_template('index.html')

@app.route('/reg', methods=['GET', 'POST'])

def reg():
	
	if request.method == 'POST':
		user = request.form.get('user')
		password = request.form.get('pass')
		
		conn = sqlite3.connect('users.db', check_same_thread=False)
		cur = conn.cursor()
		cur.execute("""CREATE TABLE IF NOT EXISTS users (
    										user TEXT NOT NULL ON CONFLICT ABORT,
    										password TEXT NOT NULL ON CONFLICT ABORT, id INT
										    DEFAULT (0) NOT NULL ON CONFLICT REPLACE);""")
		conn.commit()
		cur.execute(f'SELECT max(id) FROM users;')
		for i in cur:
			idn = i[0] + 1
		cur.execute(f'INSERT INTO users VALUES(?,?,?);', (user, password, idn))
		conn.commit()
		conn.close()

	else:
		pass
	
	return render_template('reg.html')


@app.route('/login', methods=['POST', 'GET'])

def log():

	user = request.form.get('user')
	password = request.form.get('pass')
		
	conn = sqlite3.connect('users.db', check_same_thread=False)
	cur = conn.cursor()
	cur.execute("""CREATE TABLE IF NOT EXISTS users (
    										user TEXT NOT NULL ON CONFLICT ABORT
                  							UNIQUE ON CONFLICT ABORT,
    										password TEXT NOT NULL ON CONFLICT ABORT,
										    id INT  UNIQUE ON CONFLICT ABORT
										    DEFAULT (0) NOT NULL ON CONFLICT REPLACE);""")
	conn.commit()
	cur.execute('SELECT user FROM users;')
	for fuser in cur:
		a = user
		user = (user,)
		print(fuser, user,)
		if fuser == user:
			cur.execute(f"SELECT password FROM users WHERE user = '{a}';")
			for p in cur:
				b = p
				password = (password,)
				print(p, password)
				if p == password:
					print(fuser, user, ':', p, password)
					resp = make_response()
					cur.execute(f"SELECT id FROM users WHERE user = '{a}';")
					for j in cur:
						name = str(j[0]) + a
					resp.set_cookie('user', value=name)
					if resp:
						return redirect(url_for('value'))

	return render_template('log.html')


@app.route('/authoriz')

def comp():

	return render_template('comp.html')

@app.route('/value', methods=['POST', 'GET'])

def value():

	if not request.cookies.get('user'):
		return redirect(url_for('log'))
	else:
		if request.method == 'POST':
			search = request.form.get('search')
			sub = request.form.get('sub')

			conn = sqlite3.connect('users.db', check_same_thread=False)
			cur = conn.cursor()
			cur.execute("""CREATE TABLE IF NOT EXISTS users (
    										user TEXT NOT NULL ON CONFLICT ABORT
                  							UNIQUE ON CONFLICT ABORT,
    										password TEXT NOT NULL ON CONFLICT ABORT,
										    id INT  UNIQUE ON CONFLICT ABORT
										    DEFAULT (0) NOT NULL ON CONFLICT REPLACE);""")
			conn.commit()
			cur.execute(f"SELECT user FROM users WHERE id = '{search}';")
			for i in cur:
				i = str(i[0])
				new = f'''
										  <head>
										  	<link rel="stylesheet" href="static/css/value.css">
										  </head>
										  <body><div>
											<h1>{i}</h1>
											<button class='buy'>Начать перевод</button>
										  </div>
										  <h3>В случае обмана, обращайтесь в телеграмм поддержки - @Derzilla0</h3>
										  <button onclick="location.href='http://127.0.0.1:1000/value'">Вернуться на главную</button>
										  </body>'''
				return new

	return render_template('value.html')

@app.route('/balance')
def b():
	return render_template('b.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=1000, debug=True)