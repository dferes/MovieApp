from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, URL, Optional, Length


class NewUserForm(FlaskForm):
    
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=7)])
    user_pic_url = StringField('(Optional) Image URL', validators=[URL(), Optional()])
    
    
class UserLoginForm(FlaskForm):
    
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=7)])


class EditUserForm(FlaskForm):

    username = StringField('Username')
    email = StringField('E-mail', validators=[Optional(), Email()])
    user_pic_url = StringField('Image URL', validators=[URL(), Optional()])
    bio = TextAreaField('Bio', validators=[Optional()])
    header_image_url = StringField('Header Image', validators=[URL(), Optional()])
    password = PasswordField('Password', validators=[Length(min=7), DataRequired()])
    

class NewListForm(FlaskForm):
    
    title = StringField('List Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])