# extensions.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "login"


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="user")
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # -------- Password helpers --------
    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    # -------- Utility --------
    def is_admin(self) -> bool:
        return self.role == "admin"

    def __repr__(self) -> str:
        return f"<User {self.email}>"
    
    def is_following(self, user: "User") -> bool:
        """Check if this user follows another user."""
        return Follow.query.filter_by(follower_id=self.id, followed_id=user.id).first() is not None
    
    def follow(self, user: "User") -> None:
        """Follow another user."""
        if self.id == user.id:
            return  # Cannot follow self
        if not self.is_following(user):
            association = Follow(follower_id=self.id, followed_id=user.id)
            db.session.add(association)
            db.session.commit()
    
    def unfollow(self, user: "User") -> None:
        """Unfollow another user."""
        if self.id == user.id:
            return  # Cannot unfollow self
        Follow.query.filter_by(follower_id=self.id, followed_id=user.id).delete()
        db.session.commit()
    
    def followers_count(self) -> int:
        """Get count of followers."""
        return Follow.query.filter_by(followed_id=self.id).count()
    
    def following_count(self) -> int:
        """Get count of users this user follows."""
        return Follow.query.filter_by(follower_id=self.id).count()


class Follow(db.Model):
    __tablename__ = "follows"

    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))