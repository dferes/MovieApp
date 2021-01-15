from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Follows(db.Model):
    __tablename__ = 'follows'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    following_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), primary_key=True)
    followed_by_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), primary_key=True)


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    user_pic_url = db.Column(db.Text, default="/static/images/default_user_pic.png")
    header_image_url = db.Column(db.Text, default="/static/images/default-header.jpg")
    bio = db.Column(db.Text)
    
    following = db.relationship(
        'User',
        secondary='follows',
        primaryjoin=(Follows.followed_by_id == id),
        secondaryjoin=(Follows.following_id == id)
    )
    
    followers = db.relationship(
        'User',
        secondary='follows',
        primaryjoin=(Follows.following_id == id),
        secondaryjoin=(Follows.followed_by_id == id)
    )
    
    lists = db.relationship('MovieList', backref='owning_user') # one to many, on deletion of the owner, all children will (?) also be deleted


class MovieList(db.Model):
    __tablename__ = 'movie_lists'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade')) # double check the use of cascade here
    title = db.Column(db.Text, nullable=False, unique=True)
    description = db.Column(db.Text)
    list_image_url = db.Column(db.Text)
    
    movies = db.relationship('Movie', backref='list') # one to many.
    
    
class Movie(db.Model):
    "Move or Show"
    __tablename__ = 'movies'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IMDB_id = db.Column(db.Integer, primary_key=True) # does need to be unique but not neccessarily a primary key
    list_id = db.Column(db.Integer, db.ForeignKey('movie_lists.id', ondelete='cascade'), nullable=False) # double check the use of cascade here
    name = db.Column(db.Text, nullable=False, unique=True)
    poster_url = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
