
from app import db
from models import Dislikes, Likes, User

db.drop_all()
db.create_all()

# u1 = User.signup(username = "u1",
#     password = "u1pw",
#     fullName = "u1",
#     hobbies = "running",
#     interests = "art",
#     zipcode = 90001,
#     radius = 10,
#     image = "hi.jpg")

# with open('generator/swiped.csv') as swiped:
#     db.session.bulk_insert_mappings(Swiped, DictReader(swiped))

# s1 = Swiped(
#     u1 = "u1",
#     u2="u2",
#     u1_swiped=True,
#     u2_swiped=False
# )


michael = User.signup(username="worldsbestboss",
                      password="password",
                      fullName="Michael Scott",
                      hobbies="I enjoy having breakfast in bed. I like waking up to the smell of bacon, sue me. And since I don’t have a butler, I do it myself. So, most nights before I go to bed, I will lay six strips of bacon out on my George Foreman Grill. Then I go to sleep. When I wake up, I plug in the grill, I go back to sleep again. Then I wake up to the smell of crackling bacon.",
                      interests="I love inside jokes. I'd love to be a part of one someday.",
                      zipcode=18503,
                      radius=10,
                      image="https://media.giphy.com/media/ui1hpJSyBDWlG/giphy.gif")

dwight = User.signup(username="assistantregionalmanager",
                     password="password",
                     fullName="Dwight Schrute",
                     hobbies="I love catching people in the act. That's why I always whip open doors.",
                     interests="I signed up for Second Life about a year ago. Back then, my life was so great that I literally wanted a second one. Absolutely everything was the same. Except I could fly.",
                     zipcode=18503,
                     radius=10,
                     image="https://media.giphy.com/media/wsuqQBTFD5DAq0VPQO/giphy.gif")

jim = User.signup(username="dave",
                  password="password",
                  fullName="Jim Halpert",
                  hobbies="You're looking at the master of leaving parties early.",
                  interests="From time to time I send Dwight faxes. From himself. From the future.",
                  zipcode=18503,
                  radius=10,
                  image="https://media.giphy.com/media/9o59Pga7BWlDrzWhhh/giphy.gif")

pam = User.signup(username="receptionitis15",
                  password="password",
                  fullName="Pam Beesly",
                  hobbies="There's nothing better than a beautiful day at the beach filled with sun, surf, and uh, diligent note-taking",
                  interests="You see Dwight's coffee mug? Sometimes when he's not here, I try to throw stuff in it.",
                  zipcode=18503,
                  radius=10,
                  image="https://media.giphy.com/media/AQNknFPC97yMnIdRjG/giphy.gif")

ryan = User.signup(username="wunderkind",
                   password="password",
                   fullName="Ryan Howard",
                   hobbies="WUPHF",
                   interests="I'm in love with Kelly Kapoor, and I don't know how I'm gonna feel tomorrow or the next day or the day after that, but I do know that right here, right now, all I can think about is spending the rest of my life with her. Again, that could change.",
                   zipcode=18503,
                   radius=10,
                   image="https://media.giphy.com/media/wIngWpdKeoI7Uyq3vl/giphy.gif")

andy = User.signup(username="narddog",
                   password="password",
                   fullName="Andy Bernard",
                   hobbies="I went to Cornell. Ever heard of it? I graduated in four years, I never studied once, I was drunk the whole time, and I sang in the acapella group, 'Here Comes Treble'.",
                   interests="Every little boy fantasizes about his fairytale wedding.",
                   zipcode=18503,
                   radius=10,
                   image="https://media.giphy.com/media/T9pLxAiWOTywm1H7sd/giphy.gif")

angela = User.signup(username="savebandit",
                     password="password",
                     fullName="Angela Kinsley",
                     hobbies="I do play games. I sing and I dangle things in front of my cats.",
                     interests="Sometimes, the clothes at GapKids are just too flashy. So I'm forced to go to the American Girl store and order clothes for large colonial dolls.",
                     zipcode=18503,
                     radius=10,
                     image="https://media.giphy.com/media/9P00PlgUCJxrLwYp9g/giphy.gif")


kelly = User.signup(username="thebusinessbitch",
                     password="password",
                     fullName="Kelly Kapoor",
                     hobbies="I talk a lot, so I've learned to just tune myself out.",
                     interests="Sometimes I get so bored I just want to scream, and then sometimes I actually do scream. I just sort of feel out what the situation calls for.",
                     zipcode=18503,
                     radius=10,
                     image="https://media.giphy.com/media/0hPFLMvEzvyxMdMc9i/giphy.gif")

# toby = User.signup(username="",
#                      password="password",
#                      fullName="",
#                      hobbies="",
#                      interests="",
#                      zipcode=18503,
#                      radius=10,
#                      image="")

# name = User.signup(username="",
#                      password="password",
#                      fullName="",
#                      hobbies="",
#                      interests="",
#                      zipcode=18503,
#                      radius=10,
#                      image="")














like1 = Likes(liker="worldsbestboss", likee="wunderkind")
like2 = Likes(liker="assistantregionalmanager", likee="worldsbestboss")
like3 = Likes(liker="dave", likee="receptionitis15")
like4 = Likes(liker="receptionitis15", likee="dave")
like5 = Likes(liker="narddog", likee="savebandit")
like6 = Likes(liker="savebandit", likee="assistantregionalmanager")
like7 = Likes(liker="assistantregionalmanager", likee="savebandit")


dislike1 = Dislikes(disliker="wunderkind", dislikee="worldsbestboss")
dislike2 = Dislikes(disliker="savebandit", dislikee="dave")
dislike3 = Dislikes(disliker="savebandit", dislikee="receptionitis15")
dislike4 = Dislikes(disliker="savebandit", dislikee="narddog")
dislike5 = Dislikes(disliker="wunderkind", dislikee="dave")


db.session.add(michael)
db.session.add(dwight)
db.session.add(jim)
db.session.add(pam)
db.session.add(ryan)
db.session.add(andy)
db.session.add(angela)

db.session.commit()


db.session.add(like1)
db.session.add(like2)
db.session.add(like3)
db.session.add(like4)
db.session.add(like5)
db.session.add(like6)
db.session.add(like7)

db.session.add(dislike1)
db.session.add(dislike2)
db.session.add(dislike3)
db.session.add(dislike4)
db.session.add(dislike5)

db.session.commit()
