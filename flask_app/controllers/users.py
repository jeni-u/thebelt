from flask_app import app
from flask import render_template,redirect,request,session
from flask_app.models.user import User
from flask_app.models.sighting import Sighting

from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def main():
    return render_template("login.html")

@app.route("/register")
def index():
    return render_template("register.html")

@app.route('/register_user', methods= ['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/register')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    register_user = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash
    }
    user_id = User.createUser(register_user)
    session['user_id'] = user_id
    return redirect('/dashboard')


@app.route('/login')
def loginPage():
    if 'user_id' in session:
        return redirect('/')
    return render_template('login.html')

@app.route('/login_user', methods = ['POST'])
def loginUser():
    if 'user_id' in session:
        return redirect('/')
    user = User.get_email(request.form)
    if not user:
        flash('Check your email again!', 'emailLogin')
        return redirect(request.referrer)
    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash("Invalid password!", 'passwordLogin')
        return redirect(request.referrer)
    session['user_id']= user['id']
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    sightings = Sighting.getAllSightings()
    for sighting in sightings:
        sighting['skeptic_count'] = Sighting.get_skeptic_count(sighting['id'])

    loggedUser = User.get_user_by_id({'id': session['user_id']})

    return render_template('dashboard.html', sightings=sightings, loggedUser=loggedUser)






