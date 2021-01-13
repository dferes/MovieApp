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