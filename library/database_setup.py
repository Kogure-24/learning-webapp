from flask import Flask
from models import db, User, Book, Loan
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta


def setup_database():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

        tama_user = User(
            username="tama",
            password_hash=generate_password_hash("tamapass"),
        )
        general_user = User(
            username="user1",
            password_hash=generate_password_hash("userpass"),
        )
        db.session.add_all([tama_user, general_user])
        db.session.commit()

        book1 = Book(title="プログラミングの基礎", author="Taro Yamada", isbn="978-4000000010")
        book2 = Book(title="Webデザイン入門", author="Jiro Tanaka", isbn="978-4000000027")
        book3 = Book(title="図書館の歴史", author="Saburo Sato", isbn="978-4000000034")
        book4 = Book(title="Flaskでデモアプリ", author="Hanako Ito", isbn="978-4000000041")

        db.session.add_all([book1, book2, book3, book4])
        db.session.commit()


        loan1 = Loan(
            book_id=book1.id,
            user_id=general_user.id,
            borrowed_at=datetime.now() - timedelta(days=5),
            returned_at=None,
        )
        loan2 = Loan(
            book=book2,
            user=general_user,
            borrowed_at=datetime.now() - timedelta(days=20),
            returned_at=datetime.now() - timedelta(days=15),
        )
        db.session.add_all([loan1, loan2])
        db.session.commit()

if __name__ == "__main__":
    setup_database()