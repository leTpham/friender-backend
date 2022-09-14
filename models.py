
from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

# TODO: Set method to compare whether both true,


class Swiped(db.Model):

    __tablename__ = "swiped"

    u1 = db.Column(
        db.Text,
        db.ForeignKey("users.id"),
        primary_key=True,
    )
    u2 = db.Column(
        db.Text,
        db.ForeignKey("users.id"),
        primary_key=True,
    )
    u1_swiped = db.Column(
        db.Boolean,
        nullable=True
    )
    u2_swiped = db.Column(
        db.Boolean,
        nullable=True
    )

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    username = db.Column(
        db.Text,
        primary_key=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )

    hobbies = db.Column(
        db.Text,
        nullable=False,
    )

    interests = db.Column(
        db.Text,
        nullable=False,
    )

    zipcode = db.Column(
        db.Integer,
    )

    radius = db.Column(
        db.Integer,
    )

    image = db.Column(
        db.Text,
        nullable=True,
    )

    def serialize(self):
        """Serialize to dictionary"""

        return{
            "username": self.username,
            "name": self.name,
            "hobbies" : self.hobbies,
            "interests": self.interests,
            "zipcode" : self.zipcode,
            "radius" : self.radius,
            "image" : self.image
        }

    # messages = db.relationship('Message', backref="user")
    # TODO: relationship b/t swiped & user

    # swiping = db.relationship(
    #     "User",
    #     secondary="notswiped",
    #     primaryjoin=(Swiped.u1 == id),
    #     secondaryjoin=(Swiped.u2 == id),
    #     backref="swiped",
    # )

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, username, password, name, hobbies, interests, zipcode, radius, image):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
            name=name,
            hobbies=hobbies,
            interests=interests,
            zipcode=zipcode,
            radius=radius,
            image=image
        )

        db.session.add(user)

        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If this can't find matching user (or if password is wrong), returns
        False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


# class Message(db.Model):

#     __tablename__ = "messages"

#     sender = db.Column(
#         db.Text,
#         db.ForeignKey("users.id"),
#         primary_key=True,
#     )
#     reciever = db.Column(
#         db.Text,
#         db.ForeignKey("users.id"),
#         primary_key=True,
#     )
#     msg = db.Column(
#         db.Text
#     )
#     timestamp = db.Column(
#         db.DateTime,
#         nullable=False,
#         default=datetime.utcnow,
#     )

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
