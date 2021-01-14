from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, URL, Optional, Length


class NewUserForm(FlaskForm):
    
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=7)])
    user_pic_url = StringField('(Optional) Image URL', validators=[URL(), Optional()])
    
    
class UserLoginForm(FlaskForm):
    
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=7)])
