from models import User
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()

def signup(username, email, password, user_pic_url):

    hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

    user = User(
        username=username,
        email=email,
        password=hashed_pwd,
        user_pic_url=user_pic_url
    )

    return user


def authenticate(username, password):
    user = User.query.filter_by(username=username).first()

    if user:
        is_auth = bcrypt.check_password_hash(user.password, password)
        if is_auth:
            return user

    return False


def is_followed_by(user_, other_user):
    """Is this user followed by `other_user`?"""

    found_user_list = [user for user in user_.followers if user == other_user]
    return len(found_user_list) == 1


def is_following(user_, other_user):
    """Is this user following `other_use`?"""

    found_user_list = [user for user in user_.following if user == other_user]
    return len(found_user_list) == 1
