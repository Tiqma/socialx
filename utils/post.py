from datetime import datetime
from extensions import db, User


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # relationship to user
    user = db.relationship('User', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return f"<Post {self.id} by {self.user_id}>"
