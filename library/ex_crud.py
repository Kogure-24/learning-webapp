from flask import Flask
from models import db, User
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def create():
    with app.app_context():
        user = User(
            username="Kogurey",
            password=generate_password_hash("12345qwer")
        )
        db.session.add(user)
        db.session.commit()

def read():
    with app.app_context():
        user = User.query.filter_by(id=3).first()
    if user:
        print(f'ID: {user.id}, Username: {user.username}')

def update():
    with app.app_context():
        user = User.query.filter_by(username='Kogurey').first()
    if user:
        user.username = 'ガブテク'
        db.session.commit()

def delete():
    with app.app_context():
        user = User.query.filter_by(username='Kogurey').first()
    if user:
        db.session.delete(user)
        db.session.commit()

def read_all():
    with app.app_context():
        users = User.query.all()
        for user in users:
            print(f'ID: {user.id}, Username: {user.username}')


    if __name__ == '__main__':
        create()
        read() 
        update()
        read()
        delete()
        read_all()
