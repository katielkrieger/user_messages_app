from flask_wtf import FlaskForm
from wtforms import StringField, validators

class newUserForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=1)], render_kw={"placeholder": "jdoe"})
    email = StringField('Email', [validators.Length(min=6, max=36)], render_kw={"placeholder": "john@gmail.com"})
    first_name = StringField('First name', [validators.Length(min=1)], render_kw={"placeholder": "John"})
    last_name = StringField('Last name', [validators.Length(min=1)], render_kw={"placeholder": "Doe"})

class newMessageForm(FlaskForm):
    content = StringField('Message', [validators.Length(min=1, max=500)], render_kw={"placeholder": "message"})