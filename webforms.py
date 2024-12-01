from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField,ValidationError,TextAreaField
from wtforms.validators import DataRequired,EqualTo,Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField
class PostForm(FlaskForm):
    title = StringField("Title",validators=[DataRequired()])
    author = StringField("Author")
    content = CKEditorField("Content",validators=[DataRequired()])
    slug = StringField("Slug",validators=[DataRequired()])
    submit = SubmitField("Submit")
    
class UserForm(FlaskForm):
    name = StringField("Name ",validators=[DataRequired()])
    username = StringField("User Name ",validators=[DataRequired()])
    email = StringField("Email ",validators=[DataRequired()])
    favourite_color = StringField("Favourite Color")
    about_author = TextAreaField("About Author")
    profile_pic = FileField("Profile Pic")
    password_hash = PasswordField("Password",validators=[DataRequired(),EqualTo("password_hash2",message="Passwords must match")])
    password_hash2 = PasswordField("Confirm Password",validators=[DataRequired()])
    submit = SubmitField("Submit")
class NamerForm(FlaskForm):
    name = StringField("What is your name? ",validators=[DataRequired()])
    submit = SubmitField("Submit")
class PasswordForm(FlaskForm):
    email = StringField("What is your Email? ",validators=[DataRequired()])
    password_hash = PasswordField("What is your password? ",validators=[DataRequired()])
    submit = SubmitField("Submit")
class LoginForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Submit")
class SearchForm(FlaskForm):
    searched = StringField("Searched",validators=[DataRequired()])
    
    submit = SubmitField("Submit")