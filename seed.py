from models import db, User, Follows, MovieList, Movie, Comment
from user_functions import signup

db.drop_all()
db.create_all()


dferes = signup(username='dferes',
                email='dferes23@gmail.com',
                password='password',
                user_pic_url='https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.redd.it%2Fjs2agifhb7xx.jpg&f=1&nofb=1'
               )
dferes.header_image_url = 'https://deniliquinchamber.com.au/wp-content/uploads/2017/04/header-image-1.png'
dferes.bio = 'This is by bio. Blah blah blah, this is some information about me.'

user2 = signup(username='user2',
               email='user2@gmail.com',
               password='password2',
               user_pic_url='https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fi.huffpost.com%2Fgen%2F1549371%2Fimages%2Fo-MAN-THINKING-SILHOUETTE-facebook.jpg&f=1&nofb=1'
              )
user2.header_image_url = 'https://demo.qodeinteractive.com/central/wp-content/uploads/2013/05/header.jpg'
user2.bio = 'Blah blah blah, this is my bio.'

user3 = signup(username='user3',
               email='user3@gmail.com',
               password='password3',
               user_pic_url='https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.e8BKzwcM8jj4QVStHm1ZnwHaKB%26pid%3DApi&f=1'
              )
user3.header_image_url = 'https://www.thenology.com/wp-content/uploads/2014/07/1500x500-New-York-Skyline-Twitter-Header0027.jpg'
user3.bio = 'This is some information about me, here is my bio'

db.session.add_all([dferes, user2, user3])
db.session.commit()

f1 = Follows(following_id=2, followed_by_id=1)
f2 = Follows(following_id=3, followed_by_id=1)
f3 = Follows(following_id=1, followed_by_id=2)
f4 = Follows(following_id=3, followed_by_id=2)
f5 = Follows(following_id=1, followed_by_id=3)
f6 = Follows(following_id=2, followed_by_id=3)

db.session.add_all([f1, f2, f3, f4, f5, f6])
db.session.commit()

list1 = MovieList(
        owner=1,
        title ='Scary Movies',
        description ="Scary movies from the 80's and 90's, expecially the cheesy ones.",
        list_image_url ='https://img.cinemablend.com/quill/7/f/0/2/6/b/7f026b808b59d72abbb9f51d94e807b0ec1069d9.jpg'
        )

list2 = MovieList(
        owner=1,
        title ='Bad Ass Anime',
        description ="Anime from the 90's and early 2000's",
        list_image_url ='https://dazedimg-dazedgroup.netdna-ssl.com/900/azure/dazed-prod/1290/3/1293538.jpg'
        )

list3 = MovieList(
        owner=1,
        title ='Dumb Comedy Movies',
        description ="Absolutely terrible movies, the ones you don't want people to know yo watch.",
        list_image_url ='https://www.denofgeek.com/wp-content/uploads/2014/11/dumb_and_dumber_to_1.jpg?resize=620%2C432'
        ) 

list4 = MovieList(
        owner=2,
        title ='SciFi',
        description ="SciFi movies from the 80's and 90's, especially if they're about aliens.",
        list_image_url = 'https://i.ytimg.com/vi/_yIp2huYgD8/maxresdefault.jpg'
        )

db.session.add_all([list1, list2, list3, list4])
db.session.commit()
