from flask import Flask, render_template, request, redirect, flash, abort
from extensions import db, login_manager, User
from utils.post import Post
from flask_login import login_user, logout_user, login_required, current_user
import random

app = Flask(__name__)
app.config["SECRET_KEY"] = "super-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://dbadm:P%40ssw0rd@Timpa.local/socialx?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Init extensions
db.init_app(app)
login_manager.init_app(app)

# Create tables if they don't exist (development convenience)
with app.app_context():
    db.create_all()

# Sample posts are kept for fallback; prefer DB-backed posts

@app.route("/")
def index():
    # show recent posts from DB (latest 10)
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(10).all()
    if not recent_posts:
        # fallback to sample content
        recent_posts = [
            {"user": "anna", "text": "Solen skiner idag ☀️"},
            {"user": "erik", "text": "Kodade hela natten... ☕"},
            {"user": "lisa", "text": "Någon som sett senaste serien?"}
        ]
    return render_template("index.html", posts=recent_posts)


@app.route('/post', methods=['POST'])
@login_required
def create_post():
    text = request.form.get('text', '').strip()
    if not text:
        flash('Du måste skriva något i inlägget')
        return redirect('/')

    post = Post(user_id=current_user.id, text=text)
    db.session.add(post)
    db.session.commit()

    flash('Inlägget publicerades')
    return redirect('/')


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


@app.route('/user/<int:user_id>')
def user_posts(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)

    posts = Post.query.filter_by(user_id=user_id).order_by(Post.created_at.desc()).all()
    return render_template('user.html', user=user, posts=posts)


if __name__ == "__main__":
    app.run(debug=True)
