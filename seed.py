from models import db, User, Follows, MovieList, Movie, Comment
from user_functions import signup

db.drop_all()
db.create_all()


dferes = signup(username='dferes',
                email='dferes23@gmail.com',
                password='password',
                user_pic_url=''
               )
dferes.id = 1
dferes.bio = 'This is by bio. Blah blah blah, this is some information about me.'

user2 = signup(username='user2',
               email='user2@gmail.com',
               password='password2',
               user_pic_url=''
              )
user2.id = 2
user2.bio = 'Blah blah blah, this is my bio.'

user3 = signup(username='user3',
               email='user3@gmail.com',
               password='password3',
               user_pic_url=''
              )
user3.id = 3
user3.bio = 'This is some information about me, here is my bio'

db.session.add_all([dferes, user2, user3])
db.session.commit()

f1 = Follows(id=1, following_id=2, followed_by_id=1)
f2 = Follows(id=2, following_id=3, followed_by_id=1)
f3 = Follows(id=3, following_id=1, followed_by_id=2)
f4 = Follows(id=4, following_id=3, followed_by_id=2)
f5 = Follows(id=5, following_id=1, followed_by_id=3)
f6 = Follows(id=6, following_id=2, followed_by_id=3)

db.session.add_all([f1, f2, f3, f4, f5, f6])
db.session.commit()





