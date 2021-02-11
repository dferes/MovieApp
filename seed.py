from models import db, Follows, MovieList, Movie, Comment, Actor
from user_functions import signup

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
        title ='Fantasy Films',
        description ="Fantasy movies that I grew up watching (not to be confused with scifi). A lot of medieval times stuff.",
        list_image_url ='https://i.ytimg.com/vi/shIqk_DGrMQ/maxresdefault.jpg'
        ) 

list4 = MovieList(
        owner=2,
        title ='SciFi',
        description ="SciFi movies from the 80's and 90's, especially if they're about aliens.",
        list_image_url = 'https://i.ytimg.com/vi/_yIp2huYgD8/maxresdefault.jpg'
        )

list5 = MovieList(
        owner=3,
        title ='Comedy Movies',
        description ="Some silly movies I watched growing up. A lot of stuff from the early 2000s",
        list_image_url = 'https://image.tmdb.org/t/p/original/A5HCmQrRbj2FECfjNldoKyX1Qbg.jpg'
        )

db.session.add_all([list1, list2, list3, list4, list5])
db.session.commit()


movie1 = Movie(
        IMDB_id='tt0213338',
        list_id=2, 
        name='Cowboy Bebop (TV Series 1998–1999)', 
        poster_url='https://imdb-api.com/posters/original/xDiXDfZwC6XYC6fxHI1jl3A3Ill.jpg',
        plot="""Cowboy Bebop (Japanese: カウボーイビバップ, Hepburn: Kaubōi Bibappu) is a Japanese science-fiction 
                anime television series animated by Sunrise featuring a production team led by director Shinichirō 
                Watanabe, screenwriter Keiko Nobumoto, character designer Toshihiro Kawamoto, mechanical designer 
                Kimitoshi Yamane, and composer Yoko Kanno. The twenty-six episodes ("sessions") of the series are 
                set in the year 2071, and follow the lives of a bounty hunter crew traveling in their spaceship 
                called the Bebop. Although it covers a wide range of genres throughout its run, Cowboy Bebop draws 
                most heavily from science fiction, western and noir films, and its most recurring thematic focal 
                points include adult existential ennui, loneliness and the difficulties of trying to escape one's 
                past.""")

movie2 = Movie(
        IMDB_id='tt0214341',
        list_id=2, 
        name='Dragon Ball Z (TV Series 1996–2003)', 
        poster_url='https://imdb-api.com/posters/original/dBsDWUcdfbuZwglgyeeQ9ChRoS4.jpg',
        plot="""Dragon Ball Z (Japanese: ドラゴンボールZ, Hepburn: Doragon Bōru Zetto, commonly abbreviated as DBZ) 
                is a Japanese anime television series produced by Toei Animation. It is the sequel to Dragon Ball 
                and adapts the latter 324 chapters of the original 519-chapter Dragon Ball manga series created 
                by Akira Toriyama which ran in Weekly Shōnen Jump from 1984 to 1995. Dragon Ball Z aired in Japan 
                on Fuji TV from April 1989 to January 1996, before getting dubbed in territories including the 
                United States, Canada, Australia, Europe, Asia, and Latin America. It was broadcast in at least 
                81 countries worldwide. It is part of the Dragon Ball media franchise.""")

movie3 = Movie(
        IMDB_id='tt0094625',
        list_id=2, 
        name='Akira (1988 film)', 
        poster_url='https://imdb-api.com/posters/original/5KlRFKKSbyCiyYpZSS3A6G5bW0K.jpg',
        plot="""Akira (Japanese: アキラ) is a 1988 Japanese animated post-apocalyptic cyberpunk action film 
                directed by Katsuhiro Otomo, produced by Ryōhei Suzuki and Shunzō Katō, and written by Otomo 
                and Izo Hashimoto, based on Otomo's 1982 manga of the same name. The film had a production 
                budget of ¥700 million ($5.5 million), making it the most expensive anime film at the time 
                (until it was surpassed a year later by Kiki's Delivery Service)""")

movie4 = Movie(
        IMDB_id='tt0120737',
        list_id=3, 
        name='The Lord of the Rings: The Fellowship of the Ring (2001)', 
        poster_url='https://imdb-api.com/posters/original/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg',
        plot="""The Lord of the Rings: The Fellowship of the Ring is a 2001 epic fantasy adventure film 
                directed by Peter Jackson, based on the 1954 novel The Fellowship of the Ring, the first 
                volume of J. R. R. Tolkien's The Lord of the Rings. The film is the first installment in The
                Lord of the Rings trilogy. It was produced by Barrie M. Osborne, Jackson, Fran Walsh and Tim 
                Sanders, and written by Walsh, Philippa Boyens and Jackson. The film features an ensemble 
                cast including Elijah Wood, Ian McKellen, Liv Tyler, Viggo Mortensen, Sean Astin, Cate 
                Blanchett, John Rhys-Davies, Billy Boyd, Dominic Monaghan, Orlando Bloom, Christopher Lee, 
                Hugo Weaving, Sean Bean, Ian Holm, and Andy Serkis. It is followed by The Two Towers (2002) 
                and The Return of the King (2003)""")

movie5 = Movie(
        IMDB_id='tt0167261',
        list_id=3, 
        name='The Lord of the Rings: The Two Towers (2002)', 
        poster_url='https://imdb-api.com/posters/original/5VTN0pR8gcqV3EPUHHfMGnJYN9L.jpg',
        plot="""The Lord of the Rings: The Two Towers is a 2002 epic fantasy adventure film directed by Peter 
                Jackson, based on the second volume of J. R. R. Tolkien's The Lord of the Rings. The film is 
                the second instalment in The Lord of the Rings trilogy and was produced by Barrie M. Osborne, 
                Fran Walsh and Jackson, and written by Walsh, Philippa Boyens, Stephen Sinclair and Jackson. 
                The film features an ensemble cast including Elijah Wood, Ian McKellen, Liv Tyler, Viggo 
                Mortensen, Sean Astin, Cate Blanchett, John Rhys-Davies, Bernard Hill, Christopher Lee, Billy 
                Boyd, Dominic Monaghan, Orlando Bloom, Hugo Weaving, Miranda Otto, David Wenham, Brad Dourif, 
                Karl Urban and Andy Serkis. It was preceded by The Fellowship of the Ring (2001) and followed 
                by The Return of the King (2003)""")

movie6 = Movie(
        IMDB_id='tt0167260',
        list_id=3, 
        name='The Lord of the Rings: The Return of the King (2003)', 
        poster_url='https://imdb-api.com/posters/original/rCzpDGLbOoPwLjy3OAm5NUPOTrC.jpg',
        plot="""The Lord of the Rings: The Return of the King is a 2003 epic fantasy adventure film directed by 
                Peter Jackson, based on the third volume of J. R. R. Tolkien's The Lord of the Rings. The film 
                is the final instalment in the Lord of the Rings trilogy and was produced by Barrie M. Osborne, 
                Jackson and Fran Walsh, and written by Walsh, Philippa Boyens and Jackson. Continuing the plot 
                of The Two Towers, Frodo, Sam and Gollum are making their final way toward Mount Doom in Mordor 
                in order to destroy the One Ring, unaware of Gollum's true intentions, while Gandalf, Aragorn, 
                Legolas, Gimli and the rest are joining forces together against Sauron and his legions in Minas 
                Tirith. It was preceded by The Fellowship of the Ring (2001) and The Two Towers (2002)""")

movie7 = Movie(
        IMDB_id='tt0106179',
        list_id=4, 
        name='The X-Files (TV Series 1993–2018)', 
        poster_url='https://imdb-api.com/posters/original/5BD0kiTGnDxONqdrsswTewnk6WH.jpg',
        plot="""The X-Files is an American science fiction drama television series created by Chris Carter. 
                The original television series aired from September 10, 1993 to May 19, 2002 on Fox. The 
                program spanned nine seasons, with 202 episodes. A short tenth season consisting of six 
                episodes premiered on January 24, 2016, and concluded on February 22, 2016. Following the 
                ratings success of this revival, The X-Files returned for an eleventh season of ten episodes, 
                which premiered on January 3, 2018, and concluded on March 21, 2018. In addition to the 
                television series, two feature films have been released: The 1998 film The X-Files, which took 
                place as part of the TV series continuity, and the stand-alone film The X-Files: I Want to 
                Believe, released in 2008, six years after the original television run had ended.""")

movie8 = Movie(
        IMDB_id='tt0242653',
        list_id=4, 
        name='The Matrix Revolutions (2003)', 
        poster_url='https://imdb-api.com/posters/original/cm14gG8xBghwIAy1GX0ryI2HA4U.jpg',
        plot="""The Matrix Revolutions is a 2003 American science fiction action film written and directed
                by the Wachowskis. It was the third installment of The Matrix film franchise, released six 
                months following The Matrix Reloaded. The film was released simultaneously in 60 countries on
                November 5, 2003. While being the final entry in the original trilogy of the series, the 
                Matrix storyline is continued in The Matrix Online. It was the first live-action feature film
                to be released in both regular and IMAX theaters at the same time. Despite having a mixed 
                reception from critics, the film grossed $427.3 million worldwide. A fourth Matrix film began 
                production in February 2020.""")

movie9 = Movie(
        IMDB_id='tt2543164',
        list_id=4, 
        name='Arrival (2016)', 
        poster_url='https://imdb-api.com/posters/original/x2FJsf1ElAgr63Y3PNPtJrcmpoe.jpg',
        plot="""Arrival is a 2016 American science fiction film directed by Denis Villeneuve and written by 
                Eric Heisserer. Based on the 1998 short story "Story of Your Life" by Ted Chiang, it stars 
                Amy Adams, Jeremy Renner, and Forest Whitaker. The film follows a linguist enlisted by the 
                United States Army to discover how to communicate with extraterrestrial aliens who have 
                arrived on Earth, before tensions lead to war.""")

movie10 = Movie(
        IMDB_id='tt0910936',
        list_id=5, 
        name='Pineapple Express (2008)', 
        poster_url='https://imdb-api.com/posters/original/Agnq0Q5oKO7HJBSyiINzVgrPJtZ.jpg',
        plot="""Pineapple Express is a 2008 American buddy stoner action comedy film directed by David Gordon 
                Green, written by Seth Rogen and Evan Goldberg and starring Rogen and James Franco. The plot 
                centers on a process server and his marijuana dealer as they are forced to flee from hitmen and 
                a corrupt police officer after witnessing them commit a murder. Producer Judd Apatow, who 
                previously worked with Rogen and Goldberg on Knocked Up and Superbad, assisted in developing 
                the story.""")

movie11 = Movie(
        IMDB_id='tt0103919',
        list_id=1, 
        name='Candyman (1992)', 
        poster_url='https://imdb-api.com/posters/original/n38YbNqUf5KWpMJFc4X3t0rlhg5.jpg',
        plot="""Candyman is a 1992
                American supernatural horror film, written and directed by Bernard Rose and starring Virginia 
                Madsen, Tony Todd, Xander Berkeley, Kasi Lemmons and Vanessa E. Williams. Based on the short story 
                "The Forbidden" by Clive Barker, the film follows a Chicago graduate student who was completing a 
                thesis on the urban legends and folklore which led her to the legend of the "Candyman", the ghost 
                of an artist and son of a slave who was murdered in the late 19th century for his relationship 
                with a white painter's daughter.""")
                
db.session.add_all([movie1,movie2,movie3,movie4,movie5,movie6,movie7,movie8,movie9,movie10,movie11])
db.session.commit()

comment1 = Comment(user_id=1, list_id=2, content='Here is one of my lists')
comment2 = Comment(user_id=2, list_id=2, content='Nice list, man')
comment3 = Comment(user_id=3, list_id=2, content='Blah blah blah, this is a comment.')
comment4 = Comment(user_id=2, list_id=4, content='Pretty sweet list')
comment5 = Comment(user_id=3, list_id=4, content="Meh, it's alright")
comment6 = Comment(user_id=3, list_id=3, content='This is a comment.')
comment7 = Comment(user_id=3, list_id=3, content='This is yet another comment.')
comment8 = Comment(user_id=1, list_id=5, content='Meh, overrated movies')
comment9 = Comment(user_id=2, list_id=1, content='Spooky stuff there')


db.session.add_all([comment9,comment8,comment7,comment6,comment5,comment4,comment3,comment2,comment1])
db.session.commit()

a1 = Actor(imdb_id="nm0005212", user_id=1, name='Ian McKellen')
a2 = Actor(imdb_id="nm0293509", user_id=1, name='Martin Freeman')
a3 = Actor(imdb_id="nm0035514", user_id=1, name='Richard Armitage')
a4 = Actor(imdb_id="nm0832792", user_id=1, name='Ken Stott')

db.session.add_all([a1,a2,a3,a4])
db.session.commit()
