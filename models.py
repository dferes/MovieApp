from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
    
    lists = db.relationship('MovieList', backref='owning_user')
    comments = db.relationship('Comment')
    actors = db.relationship('Actor', backref='list_owner')


class MovieList(db.Model):
    __tablename__ = 'movie_lists'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    list_image_url = db.Column(db.Text)
    
    movies = db.relationship('Movie', backref='parent_list')
    comments = db.relationship('Comment', backref='movie_list')
    
    
class Movie(db.Model):
    "Move or Show"
    __tablename__ = 'movies'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    IMDB_id = db.Column(db.Text, unique=True, nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('movie_lists.id', ondelete='cascade'), nullable=False)
    name = db.Column(db.Text, nullable=False)
    poster_url = db.Column(db.Text, nullable=False)
    plot = db.Column(db.Text, nullable=False)
    
    
class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), nullable=False)        
    list_id = db.Column(db.Integer, db.ForeignKey('movie_lists.id', ondelete='cascade'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user = db.relationship('User') #dont need this here...right? many-to-one relationship can be defined in User model


class Actor(db.Model):
    __tablename__ = 'actors'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    imdb_id = db.Column(db.Text, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), nullable=False)
    name = db.Column(db.Text, nullable=False)
