
from flask import render_template, request, jsonify, redirect, url_for

from judithApp import app
from brain import read_db

# fonctions : read / write / newfile / search / corrections 

# get userline
@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		while True:
			# strip + add caps
			user_line = request.form.get('first').strip()
			print 'user : '+user_line

			# check if line exists
			response = read_db(user_line)

			# post response
			print 'rep : '+response
			return response
	return render_template('index.html')



# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)



if __name__ == '__main__':
    app.run(debug=True)
