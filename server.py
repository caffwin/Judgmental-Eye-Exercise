"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    if 'user_id' in session:
        print('user id ' + str(session['user_id']) + 'is logged in')
    else:
        print('no one is logged in')
    return render_template('homepage.html')

@app.route('/register', methods=['GET'])
def register_form():

    return render_template('register_form.html')

@app.route('/register', methods=["POST"])
def register_process():

    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter(User.email == username).first()

    if user is not None:
        if user.password == password:
            print("Password matches username!")
            flash("Logged in")
            session["user_id"] = user.user_id # saves to session
            # allows us to show user on any page
            return redirect('/users/{}'.format(user.user_id))

        else: 
            print("Password does not match user!")
            flash("Incorrect Password")

    else: 
        print("Username added")
        flash("Username added")
        user = User(email=username, password=password)
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.user_id 
        return redirect('/users/{}'.format(user.user_id))

    return redirect('/')

@app.route('/unregister', methods=["GET"])
def unregister_process():

    # user_id = session['user_id']
    del session['user_id']
    return redirect('/')

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("users_list.html", users=users)


@app.route('/users/<user_id>')
def show_user_details(user_id):

    user = User.query.get(user_id)

    return render_template('user_details.html', user=user)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
