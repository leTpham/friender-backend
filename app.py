import os
import boto3
from dotenv import load_dotenv
# from werkzeug import secure_filename

from flask import Flask, render_template, request, flash, redirect, session, g, jsonify

from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User


load_dotenv()
AWS_ACCESS_KEY_ID=os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY=os.environ['AWS_SECRET_ACCESS_KEY']
DATABSE_URL=os.environ['DATABASE_URL']
BUCKET_NAME=os.environ['BUCKET_NAME']


CURR_USER_KEY = "curr_user"

s3 = boto3.client(
  "s3",
  "us-west-1",
  aws_access_key_id=AWS_ACCESS_KEY_ID,
  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///friender'
    # os.environ['DATABASE_URL'].replace("postgres://", "postgresql://"))
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

connect_db(app)

##############################################################################
# User signup/login/logout

def upload_image_get_url(image, username):
    #Create bucket later for this app

    # key = username
    # content_type ='image/jpeg'

    # s3 = boto3.resource('s3')
    # bucket = s3.Bucket(BUCKET_NAME)
    # bucket.upload_file(image, key)
    # location = boto3.client('s3').get_bucket_location(Bucket=BUCKET_NAME)['LocationConstraint']
    # url = "https://s3-{}.amazonaws.com/{}/{}".format (location, BUCKET_NAME, key, content_type )
    # print(url)
    # breakpoint()
    # return (url)

    key = image.filename
    bucket = BUCKET_NAME
    content_type = 'request.mimetype'
    image_file = image
    region = 'us-west-1'
    location = boto3.client('s3').get_bucket_location(Bucket=BUCKET_NAME)['LocationConstraint']

    client = boto3.client('s3',
                          region_name=region,
                          endpoint_url=f'https://{bucket}.s3.{location}.amazonaws.com',
                          aws_access_key_id= AWS_ACCESS_KEY_ID,
                          aws_secret_access_key= AWS_SECRET_ACCESS_KEY)

    # filename = secure_filename(image_file.filename)  # This is convenient to validate your filename, otherwise just use file.filename
    url = f"https://{bucket}.s3.{region}.amazonaws.com/{bucket}/{key}"
    client.put_object(Body=image_file,
                      Bucket=bucket,
                      Key=key,
                      ContentType=content_type)

    return url










@app.before_request # global user
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.username


def do_logout():
    """Log out user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.post('/signup')
def signup():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

    username = request.form["username"]
    password = request.form["password"]
    name = request.form["name"]
    hobbies = request.form["hobbies"]
    interests = request.form["interests"]
    zipcode = request.form["zipcode"]
    radius = request.form["radius"]

    # when creating file, needs to multi
    image = request.files["image"]

    # breakpoint()

    userImg = upload_image_get_url(image, username)

    # TODO: do_login(user)
    user = User.signup(
        username, password, name, hobbies, interests, zipcode, radius, userImg
    )

    serialized = user.serialize()
    db.session.commit()

    return jsonify(user = serialized)

@app.post('/login')
def login():
    username = request.json["username"]
    password = request.json["password"]

    user = User.authenticate(username, password)

    if user:
        do_login(user)
        breakpoint()
        return "yay loggedin "

@app.post('/logout')
def logout():

    if CURR_USER_KEY not in session:
        flash("You are not logged in")

    do_logout()

# ##############################################################################
# # General user routes: IF LOGGED IN

# # Show ALL users
# @app.get('/users')

# # Show one user
# @app.get('/users/<username>')


# ##############################################################################
# # Messages routes:

# # Show all messages created by currUser & sent to currUser
# @app.get('/messages')


# Create a new message
# @app.route('/messages/<username>', methods=["GET","POST"])
