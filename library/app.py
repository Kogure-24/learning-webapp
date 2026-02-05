from datetime import datetime, timedelta
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from forms import LoginForm
from flask import session, redirect, url_for, flash
from models import db, User
from werkzeug.security import check_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRET_KEY_FOR_DEVELOPMENT"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

Bootstrap5(app)
db.init_app(app)

# with app.app_context():
#     db.create_all()


# ----- ログインルート -----
@app.route("/login", methods=["GET", "POST"])
def login():
    user_id = session.get("user_id")
    if user_id:
        return redirect(url_for("index"))
    
    form = LoginForm()
    print(form.username.data)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        #user = User.query.filter_by(username=form.username.data).first()
        print(user)
        #見つけたユーザA = 入力されたユーザ名でデータベースを検索
        if user and check_password_hash(user.password_hash, form.password.data):
        #見つけたユーザAが空でない and Aのパスワードと入力されたパスワードが一致している:
            session["user_id"] = user.id #AのID
            flash("ログインに成功しました", "success")
            return redirect(url_for("index"))
        else:
            flash("ユーザーIDまたはパスワードが間違っています", "danger")
    return render_template("login.html", form=form)

# ----- ホーム画面 -----
@app.route('/')
def index():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    today = datetime.now().strftime("%Y年%m月%d日")
    return_deadline = (datetime.now() + timedelta(weeks=2)).strftime("%Y年%m月%d日")
    username = "tama"
    return render_template("index.html", today=today, return_deadline=return_deadline, username=username)

# ----- 図書リクエスト用のデータ -----
book_requests = []

# ----- 図書リクエスト画面 -----
@app.route("/request", methods=["GET", "POST"])
def request_book():
    if request.method == "POST":
        new_request = {
            "title": request.form["title"],
            "author": request.form["author"],
            "requester": request.form["requester"]
        }
        book_requests.append(new_request)
        return redirect(url_for("request_list"))  # 申請一覧画面へ
    return render_template("request_form.html")

# ----- 図書リクエスト一覧画面 -----
@app.route("/request_list")
def request_list():
    return render_template("request_list.html", book_requests=book_requests)

# ----- ログアウト -----
@app.route("/logout", methods=["POST"])
def logout():
    # セッションからログイン情報を削除
    session.clear()

    # ログインページへリダイレクト
    return redirect(url_for("login"))

# ----- サーバー起動 -----
if __name__ == '__main__':
    app.run(debug=True,port=5001)