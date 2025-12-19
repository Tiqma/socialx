from flask import Flask, render_template, request, redirect, flash
from extensions import db, login_manager, User
from flask_login import login_user, logout_user, login_required, current_user
import random

app = Flask(__name__)
app.config["SECRET_KEY"] = "super-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://dbadm:P%40ssw0rd@Timpa.local/socialx?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Init extensions
db.init_app(app)
login_manager.init_app(app)

# Sample posts
posts = [
    {"user": "anna", "text": "Solen skiner idag ☀️"},
    {"user": "erik", "text": "Kodade hela natten... ☕"},
    {"user": "lisa", "text": "Någon som sett senaste serien?"},
    {"user": "alex", "text": "Python > allt annat"},
    {"user": "sam", "text": "Vad händer i dag?"}
]

@app.route("/")
def index():
    random_posts = random.sample(posts, k=3)
    return render_template("index.html", posts=random_posts)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if User.query.filter_by(email=email).first():
            flash("Email används redan")
            return redirect("/register")

        user = User(email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect("/")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect("/")
        flash("Fel email eller lösenord")
        return redirect("/login")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route("/profile")
@login_required
def profile():
    return f"Hej {current_user.email}! Detta är din profil."

if __name__ == "__main__":
    app.run(debug=True)
