from flask import Flask, render_template, redirect, url_for, request, flash
from flask_modus import Modus
from flask_sqlalchemy import SQLAlchemy
import os
from forms import newUserForm, newMessageForm

app = Flask(__name__)
modus = Modus(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/07-sql-alchemy-2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)

class User(db.Model):

    __tablename__ = "users"

    # id, username, email, first_name, last_name
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    messages = db.relationship('Message', backref='user', lazy='dynamic')

    def __init__(self, username, email, first_name, last_name):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return "{} {}'s' username is {} and email is {}.".format(self.first_name, self.last_name, self.username, self.email)

class Message(db.Model):

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.VARCHAR(100), nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) # table name, and primary key

    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        return self.content

@app.route('/')
def root():
    return redirect(url_for('index'))

# --- USER ROUTES ---

@app.route('/users', methods=["GET", "POST"])
def index():
    form = newUserForm(request.form)
    if request.method == "POST":
        if form.validate():
            flash("You've successfully created an account!")
            new_user = User(request.form['username'], request.form['email'], request.form['first_name'], request.form['last_name'])
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            flash("Please review and correct the errors below, and then resubmit.")
            return render_template('users/new.html', form=form)

    users = User.query.all()
    return render_template('users/index.html', users=users)

@app.route('/users/new')
def new():
    form = newUserForm(request.form)
    return render_template('users/new.html', form=form)

@app.route('/users/<int:user_id>', methods=["GET","PATCH","DELETE"])
def show(user_id):
    # form = newUserForm(request.form)
    found_user = User.query.get_or_404(user_id)

    if request.method == b"PATCH":
        found_user.username = request.form['username']
        found_user.email = request.form['email']
        found_user.first_name = request.form['first_name']
        found_user.last_name = request.form['last_name']
        db.session.add(found_user)
        db.session.commit()
        return redirect(url_for('index'))

    if request.method == b"DELETE":
        db.session.delete(found_user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('users/show.html', user=found_user)


@app.route('/users/<int:user_id>/edit')
def edit(user_id):
    form = newUserForm(request.form)
    found_user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=found_user, form=form) # this lets us prepopulate the form fields

# --- MESSAGE ROUTES ---

@app.route('/users/<int:user_id>/messages', methods=["GET","POST"])
def index_msg(user_id):
    form = newMessageForm(request.form)
    if request.method == "POST":
        if form.validate():
            new_message = Message(request.form['content'],user_id)
            db.session.add(new_message)
            db.session.commit()
            return redirect(url_for('index_msg', user_id=user_id))
        else:
            flash("Please review and correct the errors below, and then resubmit.")
            return render_template('messages/new.html', form=form)

    user = User.query.get_or_404(user_id)
    return render_template('messages/index.html', user=user)

@app.route('/users/<int:user_id>/messages/new')
def new_msg(user_id):
    form = newMessageForm(request.form)
    user = User.query.get_or_404(user_id)
    return render_template('messages/new.html', user=user, form=form)

@app.route('/users/<int:user_id>/messages/<int:msg_id>', methods=["GET", "PATCH", "DELETE"])
def show_msg(user_id,msg_id):
    # form = newMessageForm(request.form)
    found_message = Message.query.get_or_404(msg_id)
    found_user = User.query.get_or_404(user_id)
    if request.method == b"PATCH":
        found_message.msg = request.form['content'] # this is updating
        # from IPython import embed; embed()
        db.session.add(found_message)
        db.session.commit() # but the database isn't???
        return redirect(url_for('index_msg', user_id=user_id))

    if request.method == b"DELETE":
        db.session.delete(found_message)
        db.session.commit()
        return redirect(url_for('index_msg', user_id=user_id))

    return render_template('messages/show.html', user=found_user, message=found_message)

@app.route('/users/<int:user_id>/messages/<int:msg_id>/edit')
def edit_msg(user_id,msg_id):
    # user = User.query.get_or_404(user_id)
    form = newMessageForm(request.form)
    found_message = Message.query.get_or_404(msg_id)
    found_user = User.query.get_or_404(user_id)
    return render_template('messages/edit.html', user=found_user, message=found_message, form=form)


# If we are in production, make sure we DO NOT use the debug mode
if os.environ.get('ENV') == 'production':
    app.config.from_object('config.ProductionConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

if __name__ == '__main__':
    app.run()