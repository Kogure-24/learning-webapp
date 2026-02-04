from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("ユーザーID", validators=[DataRequired(), Length(min=2, max=80)])
    password = PasswordField("パスワード", validators=[DataRequired()])
    submit = SubmitField("ログイン")
