
from app import db
from models import User

db.drop_all()
db.create_all()

u1 = User.signup(username = "u1",
    password = "u1pw",
    fullName = "u1",
    hobbies = "running",
    interests = "art",
    zipcode = 90001,
    radius = 10,
    image = "hi.jpg")

u2 = User.signup(username = "u2",
    password = "u2pw",
    fullName = "u2",
    hobbies = "running",
    interests = "art",
    zipcode = 90002,
    radius = 20,
    image = "hi.jpg")

# with open('generator/swiped.csv') as swiped:
#     db.session.bulk_insert_mappings(Swiped, DictReader(swiped))

# s1 = Swiped(
#     u1 = "u1",
#     u2="u2",
#     u1_swiped=True,
#     u2_swiped=False
# )


db.session.add(u1)
db.session.add(u2)

db.session.commit()

# db.session.add(s1)

db.session.commit()
