from flask import Flask
from models import db, User
from werkzeug.security import generate_password_hash
def setup_database():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

        tama_user = User(
            username='tama', 
            password_hash=generate_password_hash('tamapass'), 
        )
        general_user = User(
            username='user1', 
            password_hash=generate_password_hash('userpass'), 
        )
        db.session.add_all([tama_user, general_user])
        db.session.commit()
if __name__ == '__main__':
    setup_database()
