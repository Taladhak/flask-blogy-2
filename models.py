"""Models for Blogly."""
# connect SQLAlchemy to the flask app
from flask_sqlalchemy import SQLAlchemy
import datetime


# create a SQLAlchemy instance
db = SQLAlchemy()

# create logic to connect to the database
def connect_db(app):
    db.app = app
    db.init_app(app)

# models for the database
class User(db.Model):
    """User."""
    # table name
    __tablename__ = "users" 
    # columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(255), nullable=False, default='https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png') 

    def full_name(self):
        # return f"{self.first_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
    
class Post(db.Model);
    __tablename__ = "posts"
    id = db.column(db.Integer, primary_key=True, autoincrement=True)
    title = db.column(db.text, nullable=False)
    content = db.column(db.text, nullable=False)
    created_at = db.column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now
    )
    # foreign key
    user_id = db.column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
    
