import os
# from dotenv import load_dotenv

from flask import Flask, render_template, request, flash, redirect, session, g

from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User, Message, Like

# load_dotenv()

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ['DATABASE_URL'].replace("postgres://", "postgresql://"))
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

connect_db(app)

##############################################################################
# User signup/login/logout

@app.before_request # global user
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

# TODO: How to get form info from JS to python? request.form? 
@app.route('/signup', methods="POST")


@app.route('/login', method="POST")


@app.route('/logout', method="POST")


##############################################################################
# General user routes: IF LOGGED IN

# Show ALL users
@app.get('/users')

# Show one user
@app.get('/users/<username>')


##############################################################################
# Messages routes:

# Show all messages created by currUser & sent to currUser
@app.get('/messages')


# Create a new message
@app.route('/messages/<username>', methods=["GET","POST"])
