from flask_wtf import FlaskForm
from wtforms import StringField, validators

class newUserForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=1)])
    email = StringField('Email', [validators.Length(min=6, max=36)])
    first_name = StringField('First name', [validators.Length(min=1)])
    last_name = StringField('Last name', [validators.Length(min=1)])