
from app import db
from models import Dislikes, Likes, User

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

# u2 = User.signup(username = "u2",
#     password = "u2pw",
#     fullName = "u2",
#     hobbies = "running",
#     interests = "art",
#     zipcode = 90002,
#     radius = 20,
#     image = "hi.jpg")

u3 = User.signup(username = "u3",
    password = "u3pw",
    fullName = "u3",
    hobbies = "walking",
    interests = "eat",
    zipcode = 90003,
    radius = 3,
    image = "https://robohash.org/dictarationeesse.png?size=50x50&set=set1")

# with open('generator/swiped.csv') as swiped:
#     db.session.bulk_insert_mappings(Swiped, DictReader(swiped))

# s1 = Swiped(
#     u1 = "u1",
#     u2="u2",
#     u1_swiped=True,
#     u2_swiped=False
# )

like1 = Likes(liker = "u1", likee = "u3")
dislike1 = Dislikes(disliker="u3", dislikee="u1")

db.session.add(u1)
# db.session.add(u2)
db.session.add(u3)

db.session.commit()

db.session.add(like1)
db.session.add(dislike1)

db.session.commit()
