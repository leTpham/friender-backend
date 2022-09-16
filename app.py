import os
import boto3
from dotenv import load_dotenv
# from werkzeug import secure_filename

from flask import Flask, render_template, request, flash, redirect, session, g, jsonify
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User, Likes

import jwt

load_dotenv()
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
DATABSE_URL = os.environ['DATABASE_URL']
BUCKET_NAME = os.environ['BUCKET_NAME']
SECRET_KEY = os.environ['SECRET_KEY']

s3 = boto3.client(
    "s3",
    "us-west-1",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

app = Flask(__name__)
CORS(app)

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

@app.before_request
def add_user_to_g():
    header_token = request.headers.get('Authorization')
    print("HEADER TOKEN", header_token)
    if header_token:
        token = header_token.split(" ")[1]
        print("BEARER TOKEN", token)
        print("TOKEN:", "hi", token)
        if token:
            try:
                print("in try")
                curr_user = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                print("CURR USER")
                g.user = curr_user
            except:
                g.user = None
                print("error")
    else:
        g.user = None

def createToken(username):
    encoded_jwt = jwt.encode({"username": username} , SECRET_KEY, algorithm='HS256')
    return encoded_jwt

def upload_image_get_url(image):
    # Create bucket later for this app

    key = image.filename
    bucket = BUCKET_NAME
    content_type = 'request.mimetype'
    image_file = image
    region = 'us-west-1'
    location = boto3.client('s3').get_bucket_location(
        Bucket=BUCKET_NAME)['LocationConstraint']

    client = boto3.client('s3',
                          region_name=region,
                          endpoint_url=f'https://{bucket}.s3.{location}.amazonaws.com',
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    url = f"https://{bucket}.s3.{region}.amazonaws.com/{bucket}/{key}"
    client.put_object(Body=image_file,
                      Bucket=bucket,
                      Key=key,
                      ContentType=content_type)

    return url

@app.post('/signup')
def signup():

    username = request.form["username"]
    password = request.form["password"]
    fullName = request.form["fullName"]
    hobbies = request.form["hobbies"]
    interests = request.form["interests"]
    zipcode = int(request.form["zipcode"])
    radius = int(request.form["radius"])

    # when creating file, needs to multi
    image = request.files["image"]

    userImg = upload_image_get_url(image)

    user = User.signup(
        username, password, fullName, hobbies, interests, zipcode, radius, userImg
    )
    print("USER", user)
    print("USERNAME", username)
    print("IMAGE", image)
    # serialized = user.serialize()
    db.session.commit()

    token = createToken(username)

    return jsonify(token=token)


@app.post('/login')
def login():
    username = request.json["username"]
    password = request.json["password"]

    user = User.authenticate(username, password)
    if user == False:
        return (jsonify(message="Invalid username/password"), 401)

    token = createToken(username)

    return jsonify(token=token)

# ##############################################################################
# # General user routes: IF LOGGED IN

# # Show ALL users

@app.get('/users')
def get_all_users():

    if not g.user:
        return (jsonify(message="Not Authorized"), 401)

    current_user = User.query.get_or_404(g.user)

    already_liked_users_username = [u.username for u in current_user.liked]
    already_disliked_users_username = [u.username for u in current_user.disliked]

    invalid_usernames = already_liked_users_username + already_disliked_users_username + [current_user.username]
    valid_users = User.query.filter(
                User.username.notin_(invalid_usernames))
    # users = User.query.all()


    serialized = [u.serialize() for u in valid_users]

    return jsonify(users=serialized)


# Show one user
@app.get('/users/<username>')
def get_one_user(username):

    if not g.user:
        return (jsonify(message="Not Authorized"), 401)
    curr_user = User.query.get_or_404(g.user)
    curr_user_liked = curr_user.liked
    curr_user_disliked = curr_user.disliked

    user = User.query.get_or_404(username)
    if user in curr_user_liked or user in curr_user_disliked:
        return (jsonify(message="We met already"), 404)

    serialized = user.serialize()
    return jsonify( user= serialized)

# Like one user
@app.post('/users/<username>/like')
def like_one_user(username):

    if not g.user:
        return (jsonify(message="Not Authorized"), 401)

    liked_user = User.query.get_or_404(username)
    current_user = User.query.get_or_404(g.user)

    current_user.liked.append(liked_user)

    db.session.commit()

    # user = User.query.get_or_404(username)
    # serialized = user.serialize()

    return jsonify( "woohoo ")

# Dislike one user
@app.post('/users/<username>/dislike')
def dislike_one_user(username):

    if not g.user:
        return (jsonify(message="Not Authorized"), 401)

    disliked_user = User.query.get_or_404(username)
    current_user = User.query.get_or_404(g.user)

    current_user.disliked.append(disliked_user)

    db.session.commit()

    # user = User.query.get_or_404(username)
    # serialized = user.serialize()
    return jsonify( " sad af ")

# Matches
@app.get('/matches')
def show_matches():

    if not g.user:
        return (jsonify(message="Not Authorized"), 401)

    current_user = User.query.get_or_404(g.user)
    matches = []
    liked_by_current_user = current_user.liked
    for u in liked_by_current_user:
        if current_user in u.liked:
            matches.append(u)

    serialized=[m.serialize() for m in matches]
    return jsonify(matches=serialized)





# ##############################################################################
# # Messages routes:

# # Show all messages created by currUser & sent to currUser
# @app.get('/messages')


# Create a new message
# @app.route('/messages/<username>', methods=["GET","POST"])

