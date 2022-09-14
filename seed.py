
from app import db
from models import User

db.drop_all()
db.create_all()

u1 = User(username = "u1",
    password = "u1pw",
    name = "u1",
    hobbies = "running",
    interests = "art",
    zipcode = 90001,
    radius = 10,
    image = "hi.jpg")

# with open('generator/swiped.csv') as swiped:
#     db.session.bulk_insert_mappings(Swiped, DictReader(swiped))
db.session.add(u1)

db.session.commit()
