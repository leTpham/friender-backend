import os
import boto3
from dotenv import load_dotenv


load_dotenv()
AWS_ACCESS_KEY_ID=os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY=os.environ['AWS_SECRET_ACCESS_KEY']


from flask import Flask, render_template, request, flash, redirect, session, g

from sqlalchemy.exc import IntegrityError

# from models import db, connect_db, User, Message, Swiped


CURR_USER_KEY = "curr_user"
app = Flask(__name__)

s3 = boto3.client(
  "s3",
  "us-west-1",
  aws_access_key_id=AWS_ACCESS_KEY_ID,
  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)







# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = (
#     os.environ['DATABASE_URL'].replace("postgres://", "postgresql://"))
# app.config['SQLALCHEMY_ECHO'] = False
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
# app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

# connect_db(app)

##############################################################################
# User signup/login/logout

def upload_image_get_url(image):
    #Create bucket later for this app
    bucket_name = "lepham-test-bucket"
    key = "cat-pic"
    content_type ='image/jpeg'

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.upload_file(image, key)
    location = boto3.client('s3').get_bucket_location(Bucket=bucket_name)['LocationConstraint']
    url = "https://s3-{}.amazonaws.com/{}/{}".format (location, bucket_name, key, content_type )
    print(url)
    return (url)




@app.before_request # global user
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

# TODO: How to get form info from JS to python? request.form?
@app.route('/signup', methods=["POST"])
def signup():
    # if CURR_USER_KEY in session:
    # del session[CURR_USER_KEY]

    image = request.json["image"];
    return upload_image_get_url(image)







# @app.route('/login', method="POST")


# @app.route('/logout', method="POST")


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
