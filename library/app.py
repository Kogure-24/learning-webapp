from datetime import datetime, timedelta
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from forms import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRET_KEY_FOR_DEVELOPMENT"
Bootstrap5(app)

# ----- ログインルート -----
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.password.data == "tamapass" and form.username.data == "tama":
            flash("ログインに成功しました", "success")
            return redirect(url_for("index"))
        else:
            flash("ユーザーIDまたはパスワードが間違っています", "danger")
    return render_template("login.html", form=form)

# ----- ホーム画面 -----
@app.route('/')
def index():
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

# ----- サーバー起動 -----
if __name__ == '__main__':
    app.run(debug=True)
